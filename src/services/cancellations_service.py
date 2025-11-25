from fastapi import HTTPException
import datetime
import uuid
from sqlalchemy.orm import Session
from src.database.models.pensions import Subscriptions, Funds, Cancellations, Transactions, Notifications
from src.database.schemas.dto import CancelCreate
from src.utils.logging import logger

class CancellationService:

    def __init__(self, db: Session):
        self.db = db

    def create_cancellation(self, payload: CancelCreate):
        sub = (
            self.db.query(Subscriptions)
            .filter(Subscriptions.id_subscriptions == payload.id_subscriptions)
            .first()
        )
        if not sub:
            logger.error(
                f"Subscriptions with ID {payload.id_subscriptions} not found for cancellation."
            )
            raise HTTPException(status_code=404, detail="Subscriptions not found")
        fund = self.db.query(Funds).filter(Funds.fund_id == payload.fund_id).first()
        if not fund:
            logger.error(f"Fund with ID {payload.fund_id} not found for cancellation.")
            raise HTTPException(status_code=404, detail="Fund not found")
        canceled = Cancellations(
            client_id=payload.client_id,
            fund_id=payload.fund_id,
            id_subscriptions=payload.id_subscriptions,
            date_cancelled=datetime.datetime.now(),
            start_amount=sub.amount,
            profit=fund.annual_return * sub.amount,
        )
        self.db.add(canceled)
        self.db.commit()
        self.db.refresh(canceled)

        trx = Transactions(
            transactions_id = str(uuid.uuid4()),
            id_subscriptions = sub.id_subscriptions,
            cancelled_id = canceled.cancelled_id,
            client_id = canceled.client_id,
            fund_id = canceled.fund_id,
            date = datetime.datetime.now(),
            type = "cancellation",
            amount = sub.amount,
        )
        self.db.add(trx)
        self.db.commit()
        self.db.refresh(trx)

        notify=Notifications(
            client_id = payload.client_id,
            cancelled_id = canceled.cancelled_id,
            id_subscriptions = payload.id_subscriptions,
            sent_date = datetime.datetime.now(),
            origin = "cancellation",
        )
        self.db.add(notify)
        self.db.commit()
        self.db.refresh(notify)

        return {"cancellations": canceled,
            "transaction": trx,
            "fund": fund,
            "notification": notify}