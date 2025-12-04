
from typing import Literal
from fastapi import HTTPException
from sqlmodel import select, Session

from src.models import Stock, NpPrediction, LlmPrediction

def get_stock_prediction_controller(
    symbol: str,
    method: Literal["llm", "neuralprophet"],
    offset: int,
    limit: int,
    session: Session
):
    # Verify stock exists
    stock = session.get(Stock, symbol)
    if not stock:
        raise HTTPException(status_code=404, detail=f"Stock {symbol} not found")

    # Query latest prediction
    if method == "llm":
        all_prediction = session.exec(
            select(LlmPrediction)
            .where(LlmPrediction.symbol == symbol)
            .order_by(LlmPrediction.trade_date.desc())
            .offset(offset)
            .limit(limit)
        ).all()

        if not all_prediction:
            raise HTTPException(status_code=404, detail=f"No LLM prediction for {symbol}")

        return {
            "llm": [{
                "next_day": prediction.trade_date.isoformat(),
                "price": float(prediction.prediction_value),
                "prediction_calculated_time": prediction.created_at.isoformat(),
            } for prediction in all_prediction]
        }

    elif method == "neuralprophet":
        all_prediction = session.exec(
            select(NpPrediction)
            .where(NpPrediction.symbol == symbol)
            .order_by(NpPrediction.trade_date.desc())
            .offset(offset)
            .limit(limit)
        ).all()

        if not all_prediction:
            raise HTTPException(status_code=404, detail=f"No NeuralProphet prediction for {symbol}")

        return {
            "neuralprophet": [{
                "next_day": prediction.trade_date.isoformat(),
                "price": float(prediction.prediction_value),
                "prediction_calculated_time": prediction.created_at.isoformat(),
            } for prediction in all_prediction]
        }
