
from typing import Literal
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import select, Session

from src.models import Stock, NpPrediction, LlmPrediction
from src.config import get_session


router = APIRouter(prefix="/api/v1", tags=["API"])


@router.get("/stocks", response_model=list[Stock])
def get_stocks(session: Session = Depends(get_session)):
    """Return all stocks from the database."""
    result = session.exec(select(Stock)).all()
    return result


@router.get("/stocks/{symbol}", response_model=list[Stock])
def get_stock(
    symbol: str,
    session: Session = Depends(get_session)
):
    """Return all stocks from the database."""
    result = session.exec(select(Stock).where(Stock.symbol == symbol)).all()
    return result


@router.get("/stocks/{symbol}/prediction")
def get_stock_prediction(
    symbol: str,
    method: Literal["llm", "neuralprophet"] = Query(..., description="Prediction method"),
    session: Session = Depends(get_session)
):
    """
    Get the latest stock prediction for a given symbol and method.
    """

    # Verify stock exists
    stock = session.get(Stock, symbol)
    if not stock:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")

    # Query latest prediction
    if method == "llm":
        prediction = session.exec(
            select(LlmPrediction)
            .where(LlmPrediction.symbol == symbol)
            .order_by(LlmPrediction.trade_date.desc())
            .limit(1)
        ).first()

        if not prediction:
            raise HTTPException(status_code=404, detail=f"No LLM prediction for {symbol}")

        return {
            "llm": {
                "next_day": prediction.trade_date.isoformat(),
                "price": float(prediction.prediction_value),
                "prediction_calculated_time": prediction.created_at.isoformat(),
            }
        }

    elif method == "neuralprophet":
        prediction = session.exec(
            select(NpPrediction)
            .where(NpPrediction.symbol == symbol)
            .order_by(NpPrediction.trade_date.desc())
            .limit(1)
        ).first()

        if not prediction:
            raise HTTPException(status_code=404, detail=f"No NeuralProphet prediction for {symbol}")

        return {
            "neuralprophet": {
                "next_day": prediction.trade_date.isoformat(),
                "price": float(prediction.prediction_value),
                "prediction_calculated_time": prediction.created_at.isoformat(),
            }
        }
