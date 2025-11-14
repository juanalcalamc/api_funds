from fastapi import APIRouter, Depends, HTTPException 
from models.pensions import Subscriptions,Transactions
from schemas.dto import SubscriptionOut,SubscriptionsCreate
from typing import List
from models.database import get_db
from sqlalchemy.orm import Session
from utils.notifications import send_notification
import uuid
import datetime


router = APIRouter()

@router.post("/subscription")
def created_subscribe(payload: SubscriptionsCreate, db: Session = Depends(get_db)):
        subscriptions = Subscriptions(
                ClientId = payload.ClientId,
                FundId = payload.FundId,
                StartDate = payload.StartDate,
                Amount = payload.Amount
        )
        
        db.add(subscriptions)
        db.commit()
        db.refresh(subscriptions)

        transaction = Transactions(
        TransactionsId = str(uuid.uuid4()),
        IdSubscriptions = subscriptions.IdSubscriptions,
        CancelledId = 0,
        ClientId = subscriptions.ClientId,   
        FundId = subscriptions.FundId,
        Date=datetime.datetime.now(),
        Type="subscription",
        Amount=payload.Amount,
        ) 
        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        message = f"Subscription to fund {payload.FundId} confirmed for amount {payload.Amount}"
        send_notification(payload.Notification, message)

        return{
            "message": "Subscription created and transaction recorded",
            "subscription": subscriptions,
            "transaction": transaction
        }

@router.get("/subscription", response_model=List[SubscriptionOut])
def list_subscriptiosn(db: Session = Depends(get_db)):
    return db.query(Subscriptions).all()
       

@router.delete("/subscriptions/{subscriptions_id}", status_code=204)
def delete_fund(subscriptions_id: int, db: Session = Depends(get_db)):
    transactions = db.query(Subscriptions).filter(Subscriptions.IdSubscriptions == subscriptions_id).first()
    if not transactions:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(transactions)
    db.commit()
    return None
    