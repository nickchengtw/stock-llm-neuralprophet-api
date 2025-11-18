
from fastapi import HTTPException
from sqlmodel import select, Session

from src.models import Stock

def get_stock_controller(symbol: str, session: Session):
    result = session.exec(select(Stock).where(Stock.symbol == symbol)).first()
    if not result:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")
    return result
