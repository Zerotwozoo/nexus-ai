from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TradeCreate(BaseModel):
    instrument: str = Field(..., max_length=20)
    trade_type: str = Field(..., pattern="^(long|short)$")
    entry_price: float
    exit_price: Optional[float] = None
    quantity: float
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    fees: float = 0
    setup: Optional[str] = None
    tags: list[str] = []
    emotion_before: Optional[str] = None
    emotion_after: Optional[str] = None
    screenshot_url: Optional[str] = None
    lesson: Optional[str] = None
    entry_time: datetime
    exit_time: Optional[datetime] = None


class TradeUpdate(BaseModel):
    exit_price: Optional[float] = None
    fees: Optional[float] = None
    setup: Optional[str] = None
    tags: Optional[list[str]] = None
    emotion_before: Optional[str] = None
    emotion_after: Optional[str] = None
    screenshot_url: Optional[str] = None
    lesson: Optional[str] = None
    exit_time: Optional[datetime] = None


class TradeResponse(BaseModel):
    id: str
    instrument: str
    trade_type: str
    entry_price: float
    exit_price: Optional[float]
    quantity: float
    stop_loss: Optional[float]
    take_profit: Optional[float]
    fees: float
    pnl: Optional[float]
    pnl_percent: Optional[float]
    setup: Optional[str]
    tags: list
    emotion_before: Optional[str]
    emotion_after: Optional[str]
    lesson: Optional[str]
    entry_time: datetime
    exit_time: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class StrategyCreate(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    rules: dict = {}


class StrategyResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    rules: dict
    performance: dict

    class Config:
        from_attributes = True


class RiskCalculateRequest(BaseModel):
    account_balance: float
    risk_percent: float = Field(default=1.0, ge=0.1, le=100)
    entry_price: float
    stop_loss: float
    position_size: Optional[float] = None
