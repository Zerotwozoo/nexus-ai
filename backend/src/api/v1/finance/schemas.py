from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date


class AccountCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    type: str = Field(default="checking", pattern="^(checking|savings|credit|cash|investment)$")
    currency: str = "USD"
    balance: float = 0


class AccountResponse(BaseModel):
    id: str
    name: str
    type: str
    currency: str
    balance: float
    is_archived: bool

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    icon: Optional[str] = None
    color: Optional[str] = None
    type: str = Field(..., pattern="^(income|expense|transfer)$")
    parent_id: Optional[str] = None


class CategoryResponse(BaseModel):
    id: str
    name: str
    icon: Optional[str]
    color: Optional[str]
    type: str

    class Config:
        from_attributes = True


class TransactionCreate(BaseModel):
    account_id: str
    category_id: Optional[str] = None
    amount: float
    currency: str = "USD"
    description: Optional[str] = None
    merchant: Optional[str] = None
    type: str = Field(..., pattern="^(income|expense|transfer)$")
    date: datetime
    tags: list[str] = []
    is_recurring: bool = False
    recurrence_rule: Optional[str] = None


class TransactionResponse(BaseModel):
    id: str
    account_id: str
    category_id: Optional[str]
    amount: float
    currency: str
    description: Optional[str]
    merchant: Optional[str]
    type: str
    status: str
    date: datetime
    tags: list
    created_at: datetime

    class Config:
        from_attributes = True


class BudgetCreate(BaseModel):
    category_id: Optional[str] = None
    name: str = Field(..., min_length=1, max_length=100)
    amount: float
    period: str = Field(default="monthly", pattern="^(weekly|monthly|yearly)$")
    start_date: date
    end_date: Optional[date] = None


class BudgetResponse(BaseModel):
    id: str
    name: str
    amount: float
    period: str
    start_date: date
    end_date: Optional[date]
    spent: float = 0

    class Config:
        from_attributes = True


class SubscriptionCreate(BaseModel):
    name: str = Field(..., max_length=200)
    provider: Optional[str] = None
    amount: float
    currency: str = "USD"
    billing_cycle: str = Field(default="monthly", pattern="^(monthly|yearly|quarterly)$")
    next_billing_date: Optional[date] = None
    category: Optional[str] = None


class SubscriptionResponse(BaseModel):
    id: str
    name: str
    provider: Optional[str]
    amount: float
    currency: str
    billing_cycle: str
    next_billing_date: Optional[date]
    is_active: bool

    class Config:
        from_attributes = True
