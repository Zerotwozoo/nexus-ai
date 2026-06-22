from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import uuid
from datetime import datetime, timezone

from src.api.deps import get_db, get_current_user
from src.infrastructure.database.models import (
    User, TradingJournal, TradingStrategy,
)
from src.api.v1.trading.schemas import *

router = APIRouter(prefix="/trading", tags=["trading"])


# ── Journal ─────────────────────────────────────────────────

@router.get("/journal", response_model=list[TradeResponse])
async def list_trades(
    instrument: str = Query(None),
    trade_type: str = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(TradingJournal).where(TradingJournal.user_id == user.id)
    if instrument:
        query = query.where(TradingJournal.instrument == instrument.upper())
    if trade_type:
        query = query.where(TradingJournal.trade_type == trade_type)
    query = query.order_by(TradingJournal.entry_time.desc())
    query = query.offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)
    trades = result.scalars().all()

    # Calculate PnL for each trade if not set
    for trade in trades:
        if trade.pnl is None and trade.exit_price:
            if trade.trade_type == "long":
                trade.pnl = (trade.exit_price - trade.entry_price) * trade.quantity - trade.fees
            else:
                trade.pnl = (trade.entry_price - trade.exit_price) * trade.quantity - trade.fees
            trade.pnl_percent = round(
                (trade.pnl / (trade.entry_price * trade.quantity)) * 100, 2
            )

    return trades


@router.post("/journal", response_model=TradeResponse, status_code=201)
async def create_trade(
    request: TradeCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    trade = TradingJournal(
        user_id=user.id,
        instrument=request.instrument.upper(),
        trade_type=request.trade_type,
        entry_price=request.entry_price,
        exit_price=request.exit_price,
        quantity=request.quantity,
        stop_loss=request.stop_loss,
        take_profit=request.take_profit,
        fees=request.fees,
        setup=request.setup,
        tags=request.tags,
        emotion_before=request.emotion_before,
        emotion_after=request.emotion_after,
        screenshot_url=request.screenshot_url,
        lesson=request.lesson,
        entry_time=request.entry_time,
        exit_time=request.exit_time,
    )

    # Calculate PnL
    if trade.exit_price:
        if trade.trade_type == "long":
            trade.pnl = (trade.exit_price - trade.entry_price) * trade.quantity - trade.fees
        else:
            trade.pnl = (trade.entry_price - trade.exit_price) * trade.quantity - trade.fees
        trade.pnl_percent = round(
            (trade.pnl / (trade.entry_price * trade.quantity)) * 100, 2
        )

    db.add(trade)
    await db.flush()
    return trade


@router.patch("/journal/{trade_id}", response_model=TradeResponse)
async def update_trade(
    trade_id: str,
    request: TradeUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    trade = await db.get(TradingJournal, uuid.UUID(trade_id))
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(trade, key, value)
    if trade.exit_price:
        if trade.trade_type == "long":
            trade.pnl = (trade.exit_price - trade.entry_price) * trade.quantity - trade.fees
        else:
            trade.pnl = (trade.entry_price - trade.exit_price) * trade.quantity - trade.fees
        trade.pnl_percent = round(
            (trade.pnl / (trade.entry_price * trade.quantity)) * 100, 2
        )
    return trade


@router.delete("/journal/{trade_id}", status_code=204)
async def delete_trade(
    trade_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    trade = await db.get(TradingJournal, uuid.UUID(trade_id))
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    await db.delete(trade)


# ── Stats ───────────────────────────────────────────────────

@router.get("/stats")
async def trading_stats(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(TradingJournal).where(TradingJournal.user_id == user.id)
    )
    trades = result.scalars().all()
    total_trades = len(trades)
    winning_trades = sum(1 for t in trades if t.pnl and t.pnl > 0)
    losing_trades = sum(1 for t in trades if t.pnl and t.pnl < 0)
    total_pnl = sum(t.pnl or 0 for t in trades)

    return {
        "total_trades": total_trades,
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "winrate": round(winning_trades / total_trades * 100, 1) if total_trades else 0,
        "total_pnl": total_pnl,
        "avg_pnl": round(total_pnl / total_trades, 2) if total_trades else 0,
    }


@router.get("/stats/equity-curve")
async def equity_curve(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(TradingJournal)
        .where(TradingJournal.user_id == user.id)
        .order_by(TradingJournal.exit_time)
    )
    trades = result.scalars().all()
    equity = 0
    curve = []
    for trade in trades:
        if trade.pnl:
            equity += trade.pnl
            curve.append({
                "date": trade.exit_time.isoformat() if trade.exit_time else trade.entry_time.isoformat(),
                "equity": round(equity, 2),
            })
    return curve


# ── Strategies ──────────────────────────────────────────────

@router.get("/strategies", response_model=list[StrategyResponse])
async def list_strategies(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(TradingStrategy).where(TradingStrategy.user_id == user.id)
    )
    return result.scalars().all()


@router.post("/strategies", response_model=StrategyResponse, status_code=201)
async def create_strategy(
    request: StrategyCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    strategy = TradingStrategy(
        user_id=user.id,
        name=request.name,
        description=request.description,
        rules=request.rules,
    )
    db.add(strategy)
    await db.flush()
    return strategy


# ── Risk Calculator ─────────────────────────────────────────

@router.post("/risk/calculate")
async def calculate_risk(
    request: RiskCalculateRequest,
):
    risk_amount = request.account_balance * (request.risk_percent / 100)
    price_risk = abs(request.entry_price - request.stop_loss)
    position_size = risk_amount / price_risk if price_risk > 0 else 0
    rr_ratio = abs(request.take_profit - request.entry_price) / price_risk if request.take_profit and price_risk > 0 else 0

    return {
        "risk_amount": round(risk_amount, 2),
        "position_size": round(position_size, 4),
        "risk_per_unit": round(price_risk, 2),
        "risk_reward_ratio": round(rr_ratio, 2),
        "max_loss": round(risk_amount, 2),
    }
