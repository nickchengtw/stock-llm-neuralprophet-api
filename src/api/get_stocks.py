
from sqlmodel import select, Session

from src.models import Stock

def get_stocks_controller(session: Session):
    result = session.exec(select(Stock)).all()
    return result
