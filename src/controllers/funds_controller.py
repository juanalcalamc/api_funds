from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import get_db
from models.pensions import Funds
from schemas.dto import FundCreate, FundUpdate, FundOut
from typing import List

router = APIRouter()

@router.post("/", response_model=FundOut, status_code=201)
def create_fund(payload: FundCreate, db: Session = Depends(get_db)):
    fund = Funds(
        Name=payload.Name,
        Term=payload.Term,
        WaitingTime=payload.WaitingTime,
        Type=payload.Type,
        Active=payload.Active,
        Annual_return=payload.Annual_return
    )
    db.add(fund)
    db.commit()
    db.refresh(fund)
    return fund

@router.get("/", response_model=List[FundOut])
def list_funds(db: Session = Depends(get_db)):
    return db.query(Funds).all()


@router.get("/{fund_id}", response_model=FundOut)
def get_fund(fund_id: int, db: Session = Depends(get_db)):
    fund = db.query(Funds).filter(Funds.FundId == fund_id).first()
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")
    return fund

@router.patch("/{fund_id}", response_model=FundOut)
def update_fund(fund_id: int, payload: FundUpdate, db: Session = Depends(get_db)):
    fund = db.query(Funds).filter(Funds.FundId == fund_id).first()
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(fund, field, value)

    db.commit()
    db.refresh(fund)
    return fund

@router.delete("/{fund_id}", status_code=204)
def delete_fund(fund_id: int, db: Session = Depends(get_db)):
    fund = db.query(Funds).filter(Funds.FundId == fund_id).first()
    if not fund:
        raise HTTPException(status_code=404, detail="Fund not found")

    db.delete(fund)
    db.commit()
    return None