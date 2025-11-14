from fastapi import APIRouter,Depends,HTTPException
from schemas.dto import CancelOut,CancelCreate
from utils.notifications import send_notification
import datetime 
import uuid
from sqlalchemy.orm import Session
from typing import List
from models.database import get_db
from models.pensions import Funds, Cancellations,Transactions,Subscriptions


router = APIRouter()
@router.post("/cancellations")
def created_canceled(payload: CancelCreate, db: Session = Depends(get_db)):
    subscriptions = db.query(Subscriptions).filter(Subscriptions.IdSubscriptions == payload.IdSubscriptions).first()
    if not subscriptions:
        raise HTTPException(status_code=404, detail="Subscriptions not found")
    fund = db.query(Funds).filter(Funds.FundId == payload.FundId).first()
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")
    canceled= Cancellations(
        ClientId = payload.ClientId,
        FundId = payload.FundId,
        IdSubscriptions = payload.IdSubscriptions,
        DateCancelled = datetime.datetime.now(),
        StartAmount = subscriptions.Amount,
        Profit = fund.Annual_return * subscriptions.Amount)
    
    db.add(canceled)
    db.commit()
    db.refresh(canceled)
    transaction = Transactions(
        TransactionsId = str(uuid.uuid4()),
        IdSubscriptions = 0,
        CancelledId = canceled.CancelledId,
        ClientId = canceled.ClientId,   
        FundId = canceled.FundId,
        Date=datetime.datetime.now(),
        Type="Cancellation",
        Amount=subscriptions.Amount,
        ) 
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    

    message = f"Cliente {payload.ClientId} Cancel to fund {payload.FundId} your start amount was {canceled.StartAmount} and you finish this process  with a profit of {fund.Annual_return * canceled.StartAmount}"
    send_notification(payload.Notification, message)

    return {
        "message": "Cancellations successfully and transaction recorded",
        "cancellations": canceled,
        "transaction": transaction
    }

@router.get("/Cancellations", response_model=List[CancelOut])
def List_Cancellatiosn(db: Session = Depends(get_db)):
    return db.query(Cancellations).all()