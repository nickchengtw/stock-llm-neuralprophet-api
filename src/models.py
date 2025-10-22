
from typing import Optional, List
from sqlmodel import SQLModel, Field, String
from sqlalchemy import Column, ARRAY


class Stock(SQLModel, table=True):
    symbol: int = Field(primary_key=True)
    stock_name: str
    keywords: Optional[List[str]] = Field(default=None, sa_column=Column(ARRAY(String)))
