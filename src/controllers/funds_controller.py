from sqlalchemy.orm import Session
from models.database import get_db
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from models.pensions import funds
from schemas.dto import FundCreate, FundUpdate, FundOut
from utils.logging import logger

router = APIRouter()

@router.post("/", response_model=FundOut, status_code=201)
def create_fund(payload: FundCreate, db: Session = Depends(get_db)):
    """"
    Crea un nuevo fondo en la base de datos.
    Args:
        payload (FundCreate): Datos necesarios para crear el fondo
        db (Session, optional): Sesion de base de datos inyectada automaticamente por FastAPI mediante 
        `Depends(get_db)`. Esta sesion se utiliza para ejecutar consultas y transacciones sobre la base de datos. No es necesario pasarla manualmente al llamar al endpoint, ya que FastAPI se encarga de resolver la dependencia.
    Returns:
        funds: El fondo creado con todos sus detalles.
        
    Raises:
        HTTPException: Si ocurre algun error durante la creacion del fondo."""
    fund = funds(
        name=payload.name,
        term=payload.term,
        waiting_time=payload.waiting_time,
        type=payload.type,
        active=payload.active,
        annual_return=payload.annual_return
    )
    db.add(fund)
    db.commit()
    db.refresh(fund)
    return fund

@router.get("/", response_model=List[FundOut])
def list_funds(db: Session = Depends(get_db)):
    """
    Lista de todos los fondos en la base de datos.
    Args:
        db (Session, optional): Sesion de base de datos inyectada automaticamente por FastAPI mediante 
        `Depends(get_db)`. Esta sesion se utiliza para ejecutar consultas y transacciones sobre la base de datos. No es necesario pasarla manualmente al llamar al endpoint, ya que FastAPI se encarga de resolver la dependencia.
    Returns:
        list: Una lista de todos los fondos almacenados en la base de datos.
        """
    return db.query(funds).all()


@router.get("/{fundid}", response_model=FundOut)
def get_fund(fundid: int, db: Session = Depends(get_db)):
    """Obtiene los detalles de un fondo específico por su ID.
    Args:
        fund_id (int): ID del fondo a obtener.
        db (Session, optional): Sesion de base de datos inyectada automaticamente por FastAPI mediante 
        `Depends(get_db)`. Esta sesion se utiliza para ejecutar consultas y transacciones sobre la base de datos. No es necesario pasarla manualmente al llamar al endpoint, ya que FastAPI se encarga de resolver la dependencia.
    Returns:
        funds: Detalles del fondo solicitado.
    Raises:
        HTTPException: Si el fondo con el ID especificado no existe.
    
    """
    fund = db.query(funds).filter(funds.fund_id == fundid).first()
    if not fund:
        logger.error(f"Fund with ID {fundid} not found for cancellation.")
        raise HTTPException(status_code=404, detail="Fund not found")
    return fund

@router.patch("/{fundid}", response_model=FundOut)
def update_fund(fundid: int, payload: FundUpdate, db: Session = Depends(get_db)):
    """Actualiza los detalles de un fondo específico por su ID.
    args: 
        fund_id (int): ID del fondo a actualizar.
        payload (FundUpdate): Datos para actualizar el fondo.
        db (Session, optional): Sesion de base de datos inyectada automaticamente por FastAPI mediante 
        `Depends(get_db)`. Esta sesion se utiliza para ejecutar consultas y transacciones sobre la base de datos. No es necesario pasarla manualmente al llamar al endpoint, ya que FastAPI se encarga de resolver la dependencia.
        Returns:
        funds: El fondo actualizado con los nuevos detalles.
        Raises: 
        HTTPException: Si el fondo con el ID especificado no existe."""
    fund = db.query(funds).filter(funds.fund_id == fundid).first()
    if not fund:
        logger.error(f"Fund with ID {fundid} not found for cancellation.")
        raise HTTPException(status_code=404, detail="Fund not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(fund, field, value)

    db.commit()
    db.refresh(fund)
    return fund

@router.delete("/{fundid}", status_code=204)
def delete_fund(fundid: int, db: Session = Depends(get_db)):
    fund = db.query(funds).filter(funds.fund_id == fundid).first()
    if not fund:
        logger.error(f"Fund with ID {fundid} not found for cancellation.")
        raise HTTPException(status_code=404, detail="Fund not found")

    db.delete(fund)
    db.commit()
    return None