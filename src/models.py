
from datetime import date, datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, String, Relationship
from sqlalchemy import Column, ARRAY


class Stock(SQLModel, table=True):
    symbol: int = Field(primary_key=True)
    stock_name: str
    keywords: Optional[List[str]] = Field(default=None, sa_column=Column(ARRAY(String)))
    # Relationships
    ohlcv: List["OHLCV"] = Relationship(back_populates="stock")
    np_predictions: List["NpPrediction"] = Relationship(back_populates="stock")
    llm_predictions: List["LlmPrediction"] = Relationship(back_populates="stock")


class OHLCV(SQLModel, table=True):
    symbol: int = Field(foreign_key="stock.symbol", primary_key=True)
    trade_date: date = Field(primary_key=True)
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int
    turnover: int
    transaction_count: int

    stock: Optional["Stock"] = Relationship(back_populates="ohlcv")


class NpPrediction(SQLModel, table=True):
    symbol: int = Field(foreign_key="stock.symbol", primary_key=True)
    trade_date: date = Field(primary_key=True)
    prediction_value: float
    created_at: datetime

    # Relationship back to Stock
    stock: Optional[Stock] = Relationship(back_populates="np_predictions")


class LlmPrediction(SQLModel, table=True):
    symbol: int = Field(foreign_key="stock.symbol", primary_key=True)
    trade_date: date = Field(primary_key=True)
    prediction_value: float
    llm_name: str
    created_at: datetime

    # Relationship back to Stock
    stock: Optional[Stock] = Relationship(back_populates="llm_predictions")
