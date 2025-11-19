from fastapi import HTTPException
import datetime, uuid
from sqlalchemy.orm import Session
from models.pensions import subscriptions, funds, cancellations, transactions, notifications
from schemas.dto import CancelCreate
from utils.logging import logger

def create_cancellation(db: Session, payload: CancelCreate):
    sub = (
        db.query(subscriptions)
        .filter(subscriptions.id_subscriptions == payload.id_subscriptions)
        .first()
    )
    if not sub:
        logger.error(
            f"Subscriptions with ID {payload.id_subscriptions} not found for cancellation."
        )
        raise HTTPException(status_code=404, detail="Subscriptions not found")
    fund = db.query(funds).filter(funds.fund_id == payload.fund_id).first()
    if not fund:
        logger.error(f"Fund with ID {payload.fund_id} not found for cancellation.")
        raise HTTPException(status_code=404, detail="Fund not found")
    canceled = cancellations(
        client_id=payload.client_id,
        fund_id=payload.fund_id,
        id_subscriptions=payload.id_subscriptions,
        date_cancelled=datetime.datetime.now(),
        start_amount=sub.amount,
        profit=fund.annual_return * sub.amount,
    )
    db.add(canceled)
    db.commit()
    db.refresh(canceled)

    trx = transactions(
        transactions_id = str(uuid.uuid4()),
        id_subscriptions = sub.id_subscriptions,
        cancelled_id = canceled.cancelled_id,
        client_id = canceled.client_id,
        fund_id = canceled.fund_id,
        date = datetime.datetime.now(),
        type = "cancellation",
        amount = sub.amount,
    )
    db.add(trx)
    db.commit()
    db.refresh(trx)

    notify=notifications(
        client_id = payload.client_id,
        cancelled_id = canceled.cancelled_id,
        id_subscriptions = payload.id_subscriptions,
        sent_date = datetime.datetime.now(),
        origin = "cancellation",
    )
    db.add(notify)
    db.commit()
    db.refresh(notify)

    return canceled, trx, fund, notify