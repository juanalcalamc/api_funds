from http.client import HTTPException
from typing import Type
from sqlalchemy.orm import Session
from models.pensions import subscriptions, funds
from schemas.dto import CancelCreate
from utils.logging import logger


class CancelService:
    def __init__(self, db: Session, model: Type):
        self.db = db
        self.model = model

    def cancel_subscription(self, payload: CancelCreate):
        canceled = (
            self.db.query(subscriptions)
            .filter(subscriptions.id_subscriptions == payload.id_subscriptions)
            .first()
        )
        fund = self.db.query(funds).filter(funds.fund_id == canceled.fund_id).first()
        if not canceled:
            logger.error(
                f"Subscriptions with ID {payload.id_subscriptions} not found for cancellation."
            )
            raise HTTPException(status_code=404, detail="Subscriptions not found")
        if not fund:
            logger.error(f"Fund with ID {payload.fund_id} not found for cancellation.")
            raise HTTPException(status_code=404, detail="Fund not found")
        return canceled, fund
