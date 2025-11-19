import datetime, uuid
from fastapi import  HTTPException
from models.pensions import subscriptions, transactions, notifications
from schemas.dto import SubscriptionsCreate
from sqlalchemy.orm import Session
from utils.logging import logger

def create_subscription_transaction(db: Session, payload: SubscriptionsCreate):
    sub  = subscriptions(
        client_id=payload.client_id,
        fund_id=payload.fund_id,
        start_date=payload.start_date,
        amount=payload.amount,
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)
    trx = transactions(
        transactions_id = str(uuid.uuid4()),
        id_subscriptions = sub .id_subscriptions,
        cancelled_id = 0,
        client_id = sub.client_id,
        fund_id = sub.fund_id,
        date = datetime.datetime.now(),
        type = "subscription",
        amount = sub.amount,
    )
    db.add(trx)
    db.commit()
    db.refresh(trx)

    notify=notifications(
        client_id = payload.client_id,
        cancelled_id = 0,
        id_subscriptions = sub.id_subscriptions,
        sent_date = datetime.datetime.now(),
        origin = "subscription",
    )
    db.add(notify)
    db.commit()
    db.refresh(notify)
    return sub, trx, notify

def delete_subscription(db: Session, subscription_id: int):
    delete_sub = (
        db.query(subscriptions)
        .filter(subscriptions.id_subscriptions == subscription_id)
        .first()
    )
    if not delete_sub:
        logger.error(f"Subscriptions with ID {subscription_id} not found.")
        raise HTTPException(status_code=404, detail="Subscription not found")

    db.delete(delete_sub)
    db.commit()
    return delete_sub