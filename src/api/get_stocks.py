
from fastapi import APIRouter, Depends
from sqlmodel import select, Session

from src.models import Stock
from src.config import get_session


router = APIRouter(prefix="/api/v1", tags=["API"])


@router.get("/stocks", response_model=list[Stock])
def get_stocks(session: Session = Depends(get_session)):
    """Return all stocks from the database."""
    result = session.exec(select(Stock)).all()
    return result
