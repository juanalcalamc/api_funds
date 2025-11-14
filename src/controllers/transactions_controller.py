from fastapi import APIRouter, Depends, HTTPException
from schemas.dto import TransactionsOut
from models.pensions import Transactions
from typing import List
from models.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/transactions", response_model=List[TransactionsOut])
def List_Transactions(db: Session = Depends(get_db)):
    return db.query(Transactions).all()
       

@router.delete("/transactions/{transactions_id}", status_code=204)
def delete_fund(transactions_id: str, db: Session = Depends(get_db)):
    transactions = db.query(Transactions).filter(Transactions.TransactionsId == transactions_id).first()
    if not transactions:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(transactions)
    db.commit()
    return None
    