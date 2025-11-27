
from typing import Literal
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from src.models import Stock
from src.config import get_session
from src.api.get_stocks import get_stocks_controller
from src.api.get_stock import get_stock_controller
from src.api.get_stock_prices import get_stock_prices_controller
from src.api.get_stock_prediction import get_stock_prediction_controller

router = APIRouter(prefix="/api/v1", tags=["API"])


@router.get("/stocks", response_model=list[Stock])
def get_stocks(session: Session = Depends(get_session)):
    return get_stocks_controller(session)


@router.get("/stocks/{symbol}", response_model=Stock)
def get_stock(
    symbol: str,
    session: Session = Depends(get_session)
):
    return get_stock_controller(symbol, session)


@router.get("/stocks/{symbol}/prices")
def get_stock_prices(
    symbol: str,
    session: Session = Depends(get_session),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return")
):
    return get_stock_prices_controller(symbol, session, offset, limit)


@router.get("/stocks/{symbol}/prediction")
def get_stock_prediction(
    symbol: str,
    method: Literal["llm", "neuralprophet"] = Query(..., description="Prediction method"),
    session: Session = Depends(get_session)
):
    return get_stock_prediction_controller(symbol, method, session)
