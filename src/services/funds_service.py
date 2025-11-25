from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.database.models.pensions import Funds
from src.database.schemas.dto import FundCreate, FundUpdate
from src.utils.logging import logger

class FundService:

    def __init__(self, db: Session):
        self.db = db

    def create_funds(self, payload: FundCreate):
        fund = Funds(
            name = payload.name,
            term = payload.term,
            waiting_time = payload.waiting_time,
            type = payload.type,
            active = payload.active,
            annual_return = payload.annual_return,
        )
        self.db.add(fund)
        self.db.commit()
        self.db.refresh(fund)
        return  fund

    def get_fund_by_id(self, fundid: int):

        fund = self.db.query(Funds).filter(Funds.fund_id == fundid).first()
        if not fund:
            logger.error(f"Fund with ID {fundid} not found for cancellation.")
            raise HTTPException(status_code=404, detail="Fund not found")
        return fund

    def update_funds(self, fundid: int, payload: FundUpdate):
        fund = self.db.query(Funds).filter(Funds.fund_id == fundid).first()
        if not fund:
            logger.error(f"Fund with ID {fundid} not found for cancellation.")
            raise HTTPException(status_code=404, detail="Fund not found")
        update_data = payload.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(fund, field, value)
        self.db.commit()
        self.db.refresh(fund)
        return  fund

    def delete_funds(self, fundid: int):
        fund = self.db.query(Funds).filter(Funds.fund_id == fundid).first()
        if not fund:
            logger.error(f"Fund with ID {fundid} not found for cancellation.")
            raise HTTPException(status_code=404, detail="Fund not found")
        self.db.delete(fund)
        self.db.commit()
        return fund