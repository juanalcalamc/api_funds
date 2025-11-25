import datetime
import uuid
from fastapi import  HTTPException
from sqlalchemy.orm import Session
from src.database.models.pensions import Subscriptions, Transactions, Notifications
from src.database.schemas.dto import SubscriptionsCreate
from src.utils.logging import logger

class SubscriptionService:

    def __init__(self, db: Session):
        self.db = db

    def create_subscription_transaction(self, payload: SubscriptionsCreate):
        sub  = Subscriptions(
            client_id=payload.client_id,
            fund_id=payload.fund_id,
            start_date=payload.start_date,
            amount=payload.amount,
        )
        self.db.add(sub)
        self.db.commit()
        self.db.refresh(sub)
        trx = Transactions(
            transactions_id = str(uuid.uuid4()),
            id_subscriptions = sub .id_subscriptions,
            cancelled_id = 0,
            client_id = sub.client_id,
            fund_id = sub.fund_id,
            date = datetime.datetime.now(),
            type = "subscription",
            amount = sub.amount,
        )
        self.db.add(trx)
        self.db.commit()
        self.db.refresh(trx)

        notify=Notifications(
            client_id = payload.client_id,
            cancelled_id = 0,
            id_subscriptions = sub.id_subscriptions,
            sent_date = datetime.datetime.now(),
            origin = "subscription",
        )
        self.db.add(notify)
        self.db.commit()
        self.db.refresh(notify)
        return sub, trx, notify

    def delete_subscription(self, subscription_id: int):
        delete_sub = (
            self.db.query(Subscriptions)
            .filter(Subscriptions.id_subscriptions == subscription_id)
            .first()
        )
        if not delete_sub:
            logger.error(f"Subscriptions with ID {subscription_id} not found.")
            raise HTTPException(status_code=404, detail="Subscription not found")

        self.db.delete(delete_sub)
        self.db.commit()
        return delete_sub