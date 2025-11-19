from http.client import HTTPException
from sqlalchemy.orm import Session
from models.pensions import funds
from schemas.dto import FundCreate, FundUpdate, FundOut
from utils.logging import logger

def create_funds(db: Session, payload: FundCreate):
    fund = funds(
        name = payload.name,
        term = payload.term,
        waiting_time = payload.waiting_time,
        type = payload.type,
        active = payload.active,
        annual_return = payload.annual_return,
    )
    db.add(fund)
    db.commit()
    db.refresh(fund)
    return fund

def get_fund_by_id(db: Session, fundid: int):

    fund = db.query(funds).filter(funds.fund_id == fundid).first()
    if not fund:
        logger.error(f"Fund with ID {fundid} not found for cancellation.")
        raise HTTPException(status_code=404, detail="Fund not found")
    return fund

def update_funds(db: Session, fundid: int, payload: FundUpdate):
    fund = db.query(funds).filter(funds.fund_id == fundid).first()
    if not fund:
        logger.error(f"Fund with ID {fundid} not found for cancellation.")
        raise HTTPException(status_code=404, detail="Fund not found")
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(fund, field, value)
    db.commit()
    db.refresh(fund)
    return fund

def delete_funds(db: Session, fundid: int):
    fund = db.query(funds).filter(funds.fund_id == fundid).first()
    if not fund:
        logger.error(f"Fund with ID {fundid} not found for cancellation.")
        raise HTTPException(status_code=404, detail="Fund not found")
    db.delete(fund)
    db.commit()
    return None

