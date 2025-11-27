
from fastapi import HTTPException
from sqlmodel import select, Session

from src.models import OHLCV

def get_stock_prices_controller(symbol: str, session: Session, skip, limit):
    result = session.exec(select(OHLCV.close_price, OHLCV.trade_date).offset(skip).limit(limit).where(OHLCV.symbol == symbol).order_by(OHLCV.trade_date.desc())).mappings().all()
    if not result:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")
    return result
