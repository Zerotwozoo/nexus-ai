from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
import uuid
from datetime import datetime, timezone

from src.api.deps import get_db, get_current_user
from src.infrastructure.database.models import (
    User, WorkspaceMember,
    FinanceAccount, FinanceTransaction, FinanceCategory,
    Budget, Subscription,
)
from src.api.v1.finance.schemas import *

router = APIRouter(prefix="/finance", tags=["finance"])


async def verify_access(workspace_id: str, user: User, db: AsyncSession):
    result = await db.execute(
        select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == uuid.UUID(workspace_id),
            WorkspaceMember.user_id == user.id,
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=403, detail="Access denied")


# ── Accounts ────────────────────────────────────────────────

@router.get("/accounts", response_model=list[AccountResponse])
async def list_accounts(
    workspace_id: str = Query(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await verify_access(workspace_id, user, db)
    result = await db.execute(
        select(FinanceAccount).where(
            FinanceAccount.workspace_id == uuid.UUID(workspace_id),
            FinanceAccount.is_archived == False,
        )
    )
    return result.scalars().all()


@router.post("/accounts", response_model=AccountResponse, status_code=201)
async def create_account(
    request: AccountCreate,
    workspace_id: str = Query(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await verify_access(workspace_id, user, db)
    account = FinanceAccount(
        workspace_id=uuid.UUID(workspace_id),
        name=request.name,
        type=request.type,
        currency=request.currency,
        balance=request.balance,
    )
    db.add(account)
    await db.flush()
    return account


# ── Transactions ────────────────────────────────────────────

@router.get("/transactions", response_model=list[TransactionResponse])
async def list_transactions(
    workspace_id: str = Query(...),
    account_id: str = Query(None),
    category_id: str = Query(None),
    type: str = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await verify_access(workspace_id, user, db)
    query = select(FinanceTransaction).join(FinanceAccount).where(
        FinanceAccount.workspace_id == uuid.UUID(workspace_id)
    )
    if account_id:
        query = query.where(FinanceTransaction.account_id == uuid.UUID(account_id))
    if category_id:
        query = query.where(FinanceTransaction.category_id == uuid.UUID(category_id))
    if type:
        query = query.where(FinanceTransaction.type == type)
    query = query.order_by(FinanceTransaction.date.desc())
    query = query.offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/transactions", response_model=TransactionResponse, status_code=201)
async def create_transaction(
    request: TransactionCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    tx = FinanceTransaction(
        account_id=uuid.UUID(request.account_id),
        category_id=uuid.UUID(request.category_id) if request.category_id else None,
        created_by=user.id,
        amount=request.amount,
        currency=request.currency,
        description=request.description,
        merchant=request.merchant,
        type=request.type,
        date=request.date,
        tags=request.tags,
        is_recurring=request.is_recurring,
        recurrence_rule=request.recurrence_rule,
    )
    db.add(tx)
    await db.flush()

    account = await db.get(FinanceAccount, uuid.UUID(request.account_id))
    if account:
        if request.type == "income":
            account.balance += request.amount
        elif request.type == "expense":
            account.balance -= request.amount

    return tx


# ── Categories ──────────────────────────────────────────────

@router.get("/categories", response_model=list[CategoryResponse])
async def list_categories(
    workspace_id: str = Query(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await verify_access(workspace_id, user, db)
    result = await db.execute(
        select(FinanceCategory).where(
            FinanceCategory.workspace_id == uuid.UUID(workspace_id)
        )
    )
    return result.scalars().all()


@router.post("/categories", response_model=CategoryResponse, status_code=201)
async def create_category(
    request: CategoryCreate,
    workspace_id: str = Query(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await verify_access(workspace_id, user, db)
    cat = FinanceCategory(
        workspace_id=uuid.UUID(workspace_id),
        name=request.name,
        icon=request.icon,
        color=request.color,
        type=request.type,
        parent_id=uuid.UUID(request.parent_id) if request.parent_id else None,
    )
    db.add(cat)
    await db.flush()
    return cat


# ── Budgets ─────────────────────────────────────────────────

@router.get("/budgets", response_model=list[BudgetResponse])
async def list_budgets(
    workspace_id: str = Query(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await verify_access(workspace_id, user, db)
    result = await db.execute(
        select(Budget).where(Budget.workspace_id == uuid.UUID(workspace_id))
    )
    budgets = result.scalars().all()

    # Calculate spent for each budget
    for budget in budgets:
        spent_result = await db.execute(
            select(func.sum(FinanceTransaction.amount)).where(
                FinanceTransaction.category_id == budget.category_id,
                FinanceTransaction.type == "expense",
            )
        )
        budget.spent = spent_result.scalar() or 0

    return budgets


@router.post("/budgets", response_model=BudgetResponse, status_code=201)
async def create_budget(
    request: BudgetCreate,
    workspace_id: str = Query(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await verify_access(workspace_id, user, db)
    budget = Budget(
        workspace_id=uuid.UUID(workspace_id),
        category_id=uuid.UUID(request.category_id) if request.category_id else None,
        name=request.name,
        amount=request.amount,
        period=request.period,
        start_date=request.start_date,
        end_date=request.end_date,
    )
    db.add(budget)
    await db.flush()
    return budget


# ── Subscriptions ───────────────────────────────────────────

@router.get("/subscriptions", response_model=list[SubscriptionResponse])
async def list_subscriptions(
    workspace_id: str = Query(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await verify_access(workspace_id, user, db)
    result = await db.execute(
        select(Subscription).where(
            Subscription.workspace_id == uuid.UUID(workspace_id),
            Subscription.is_active == True,
        )
    )
    return result.scalars().all()


@router.post("/subscriptions", response_model=SubscriptionResponse, status_code=201)
async def create_subscription(
    request: SubscriptionCreate,
    workspace_id: str = Query(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await verify_access(workspace_id, user, db)
    sub = Subscription(
        workspace_id=uuid.UUID(workspace_id),
        name=request.name,
        provider=request.provider,
        amount=request.amount,
        currency=request.currency,
        billing_cycle=request.billing_cycle,
        next_billing_date=request.next_billing_date,
        category=request.category,
    )
    db.add(sub)
    await db.flush()
    return sub


@router.delete("/subscriptions/{sub_id}", status_code=204)
async def delete_subscription(
    sub_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    sub = await db.get(Subscription, uuid.UUID(sub_id))
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    sub.is_active = False


# ── Analytics ───────────────────────────────────────────────

@router.get("/analytics/overview")
async def analytics_overview(
    workspace_id: str = Query(...),
    months: int = Query(3, ge=1, le=12),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await verify_access(workspace_id, user, db)

    income_result = await db.execute(
        select(func.sum(FinanceTransaction.amount)).where(
            FinanceTransaction.type == "income",
        )
    )
    expense_result = await db.execute(
        select(func.sum(FinanceTransaction.amount)).where(
            FinanceTransaction.type == "expense",
        )
    )
    total_income = income_result.scalar() or 0
    total_expense = expense_result.scalar() or 0

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_savings": total_income - total_expense,
        "savings_rate": round((total_income - total_expense) / total_income * 100, 1) if total_income else 0,
    }


@router.get("/analytics/spending")
async def analytics_spending(
    workspace_id: str = Query(...),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await verify_access(workspace_id, user, db)
    result = await db.execute(
        select(
            FinanceCategory.name,
            func.sum(FinanceTransaction.amount).label("total"),
        )
        .join(FinanceTransaction, FinanceTransaction.category_id == FinanceCategory.id)
        .where(
            FinanceTransaction.type == "expense",
        )
        .group_by(FinanceCategory.name)
    )
    rows = result.all()
    return [{"category": name, "amount": float(total)} for name, total in rows]
