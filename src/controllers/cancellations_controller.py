from sqlalchemy.orm import Session
from src.database.models.database import get_db
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from src.database.schemas.dto import CancelOut, CancelCreate, TransactionsOut
from src.utils.notifications import Email, SMS, NotificationContext
from src.database.models.pensions import  Cancellations
from src.services.cancellations_service import CancellationService
from src.utils.logging import logger

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
    service = CancellationService(db)
    result= service.create_cancellation(payload)
    canceled = result["cancellations"]
    trx = result["transaction"]
    fund = result["fund"]
    notify = result["notification"]
    
    message =( f"Client {payload.client_id} Cancel to fund {payload.fund_id} your start amount was {canceled.start_amount} and you finish this process  with a profit of {fund.annual_return * canceled.start_amount}")
    
    strategies = {"email": Email, "sms": SMS}
    if payload.notification not in strategies:
        logger.error(f"Notifications {payload.notification} canceled.")
        raise (HTTPException(status_code=404, detail="Notification method not found"))
    context = NotificationContext(strategies[payload.notification]())
    context.send_notification(message)
    logger.info(f"Cancellation created for subscription ID {payload.id_subscriptions} and transaction recorded.")
    return {
        "message": "Cancellations successfully and transaction recorded",
        "cancellations": canceled,
        "transaction": TransactionsOut.model_validate(trx),
        "notification": notify,
    }

@router.get("/cancellations", response_model=List[CancelOut])
def list_cancellations(db: Session = Depends(get_db)):
    """Lista de todas las cancelaciones en la base de datos
    args:
        db (Session, optional): Sesion de base de datos inyectada automaticamente por FastAPI mediante
        `Depends(get_db)`. Esta sesion se utiliza para ejecutar consultas y transacciones sobre la base de datos. No es necesario pasarla manualmente al llamar al endpoint, ya que FastAPI se encarga de resolver la dependencia.
    Returns:
        list: Una lista de todas las cancelaciones almacenadas en la base de datos.
    """
    return db.query(Cancellations).all()