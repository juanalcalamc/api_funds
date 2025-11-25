from sqlalchemy.orm import Session
from typing import List
from src.database.models.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from src.database.schemas.dto import TransactionsOut
from src.database.models.pensions import Transactions
from src.utils.logging import logger

router = APIRouter()

@router.get("/transactions", response_model=List[TransactionsOut])
def list_transactions(db: Session = Depends(get_db)):
    return db.query(Transactions).all()

@router.delete("/transactions/{transactionsid}", status_code=204)
def delete_fund(transactionsid: str, db: Session = Depends(get_db)):
    transactions = (
        db.query(Transactions)
        .filter(Transactions.transactions_id == transactionsid)
        .first()
    )
    if not transactions:
        logger.error(f"Transactions with ID {transactionsid} not found.")
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(transactions)
    db.commit()
    return {"message": "Transaction deleted successfully", 
            "transactions_id": transactionsid
            }