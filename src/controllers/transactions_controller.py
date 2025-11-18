from sqlalchemy.orm import Session
from typing import List
from models.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from schemas.dto import TransactionsOut
from models.pensions import transactions
from utils.logging import logger

router = APIRouter()

@router.get("/transactions", response_model=List[TransactionsOut])
def list_transactions(db: Session = Depends(get_db)):
    return db.query(transactions).all()

@router.delete("/transactions/{transactionsid}", status_code=204)
def delete_fund(transactionsid: str, db: Session = Depends(get_db)):
    Transactions = (
        db.query(transactions)
        .filter(transactions.transactions_id == transactionsid)
        .first()
    )
    if not Transactions:
        logger.error(f"Transactions with ID {transactionsid} not found.")
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(Transactions)
    db.commit()
    return None