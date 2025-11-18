import datetime 
import uuid
from sqlalchemy.orm import Session
from models.database import get_db
from typing import List
from fastapi import APIRouter,Depends,HTTPException
from schemas.dto import CancelOut,CancelCreate
from utils.notifications import Email, SMS , NotificationContext
from models.pensions import funds, cancellations,transactions,subscriptions
from utils.logging import logger


router = APIRouter()
@router.post("/cancellations")
def created_canceled(payload: CancelCreate, db: Session = Depends(get_db)):
    """Crea una cancelacion que se hace a una suscripcion existente
    
    Args:
        payload (CancelCreate): Datos necesarios para crear la cancelacion
        db (Session, optional): Sesion de base de datos inyectada automaticamente por FastAPI mediante 
        `Depends(get_db)`. Esta sesion se utiliza para ejecutar consultas y transacciones sobre la base de datos. No es necesario pasarla manualmente al llamar al endpoint, ya que FastAPI se encarga de resolver la dependencia.
        Returns:
        dict: Un diccionario con un mensaje de confirmacion y los datos de la cancelacion creada.
        
        Raises:
            HTTPException: Si ocurre algun error durante la creacion de la cancelacion, por ejemplo si la suscripcion o fondo no existen."""
    Subscriptions = db.query(subscriptions).filter(subscriptions.id_subscriptions == payload.id_subscriptions).first()
    if not Subscriptions:
        logger.error(f"Subscriptions with ID {payload.id_subscriptions} not found for cancellation.")
        raise HTTPException(status_code=404, detail="Subscriptions not found")
    fund = db.query(funds).filter(funds.fund_id == payload.fund_id).first()
    if not fund:
        logger.error(f"Fund with ID {payload.fund_id} not found for cancellation.")
        raise HTTPException(status_code=404, detail="Fund not found")
    canceled= cancellations(
        client_id = payload.client_id,
        fund_id = payload.fund_id,
        id_subscriptions = payload.id_subscriptions,
        date_cancelled = datetime.datetime.now(),
        start_amount = Subscriptions.amount,
        profit = fund.annual_return * Subscriptions.amount
        )
    
    db.add(canceled)
    db.commit()
    db.refresh(canceled)
    Transaction = transactions(
        transactions_id = str(uuid.uuid4()),
        id_subscriptions = 0,
        cancelled_id = canceled.cancelled_id,
        client_id = canceled.client_id,   
        fund_id = canceled.fund_id,
        date=datetime.datetime.now(),
        type="cancellation",
        amount=Subscriptions.amount,
        ) 
    db.add(Transaction)
    db.commit()
    db.refresh(Transaction)

    

    message = f"Client {payload.client_id} Cancel to fund {payload.fund_id} your start amount was {canceled.start_amount} and you finish this process  with a profit of {fund.annual_return * canceled.start_amount}"
    strategies = {
        'Email': Email,
        'SMS': SMS
    }
    if payload.notification not in strategies:
        logger.error(f"Notifications {payload.notification} canceled.")
        raise(HTTPException(status_code=404, detail="Notification method not found"))
    
    context = NotificationContext(strategies[payload.notification]())
    context.send_notification(message)

    return {
        "message": "Cancellations successfully and transaction recorded",
        "cancellations": canceled,
        "transaction": Transaction
    }

@router.get("/Cancellations", response_model=List[CancelOut])
def List_Cancellatiosn(db: Session = Depends(get_db)):
    """Lista de todas las cancelaciones en la base de datos
    args:
        db (Session, optional): Sesion de base de datos inyectada automaticamente por FastAPI mediante 
        `Depends(get_db)`. Esta sesion se utiliza para ejecutar consultas y transacciones sobre la base de datos. No es necesario pasarla manualmente al llamar al endpoint, ya que FastAPI se encarga de resolver la dependencia.
    Returns:
        list: Una lista de todas las cancelaciones almacenadas en la base de datos.
    """
    return db.query(cancellations).all()