from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from models.pensions import subscriptions
from schemas.dto import SubscriptionOut, SubscriptionsCreate,TransactionsOut
from models.database import get_db
from utils.notifications import Email, SMS, NotificationContext
from utils.logging import logger
from services.subscriptions_service import create_subscription_transaction, delete_subscription

router = APIRouter()

@router.post("/subscription")
def created_subscribe(payload: SubscriptionsCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva suscripción en la base de datos.
    Args:
        payload (SubscriptionsCreate):
            contiene los datos necesarios para crear la suscripción
            (ClientId, FundId, Amount, StartDate, etc.).
        db (Session, optional):
            Sesión de base de datos inyectada automáticamente por FastAPI mediante
            `Depends(get_db)`. Esta sesión se utiliza para ejecutar consultas y
            transacciones sobre la base de datos. No es necesario pasarla manualmente
            al llamar al endpoint, ya que FastAPI se encarga de resolver la dependencia.
    Returns:
        dict:
            Un diccionario con un mensaje de confirmación y los datos de la suscripción creada.
    Raises:
        HTTPException:
            Si ocurre algún error durante la creación de la suscripción, por ejemplo
            si el fondo o cliente no existen.
    """
    try:
        sub, trx, notify = create_subscription_transaction(db, payload)
        message = (
            f"Subscription to fund {payload.fund_id} confirmed for amount {payload.amount}"
        )
        strategies = {"email": Email, "sms": SMS}
        if payload.notification not in strategies:
            logger.error(
                f"The notification with the {payload.notification} type could not be sent."
            )
            raise (HTTPException(status_code=404, detail="Notification method not found"))
        context = NotificationContext(strategies[payload.notification]())
        context.send_notification(message)
        return {
            "logger": logger.info(f"Subscription created successfully with ID {sub.id_subscriptions}."),
            "message": "Subscription created and transaction recorded",
            "subscription": SubscriptionOut.model_validate(sub),
            "transaction": TransactionsOut.model_validate(trx),
            "notifications": notify
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/subscription", response_model=List[SubscriptionOut])
def list_subscriptions(db: Session = Depends(get_db)):
    """
    Trae una lista de todas las suscripciones almacenadas en la base de datos.
    Args:
        db (Session, optional):
            Sesión de base de datos inyectada automáticamente por FastAPI mediante
            `Depends(get_db)`. Esta sesión se utiliza para ejecutar consultas y
            transacciones sobre la base de datos. No es necesario pasarla manualmente
            al llamar al endpoint, ya que FastAPI se encarga de resolver la dependencia.
    Returns:
        list[SubscriptionOut]:
            retorna una lista de todas las suscripciones en la base de datos."""
    return db.query(subscriptions).all()

@router.delete("/subscriptions/{subscriptionsid}", status_code=204)
def delete_subs(subscriptionsid: int, db: Session = Depends(get_db)):
    """
    Elimina una suscripción específica de la base de datos según su ID.
    Args:
        db (Session, optional):
            Sesión de base de datos inyectada automáticamente por FastAPI mediante
            `Depends(get_db)`. Esta sesión se utiliza para ejecutar consultas y
            transacciones sobre la base de datos. No es necesario pasarla manualmente
            al llamar al endpoint, ya que FastAPI se encarga de resolver la dependencia.
    Raises:
        HTTPException:
            Si ocurre algún error durante la eliminacion de la suscripción, por ejemplo
            si la suscripcion no existen.
    """
    try:
        delete_sub = delete_subscription(db, subscriptionsid)
        return {"deleted_subscription": delete_sub}
    except Exception as e:
        logger.exception(f"error deleting subscription {subscriptionsid}")
        raise HTTPException(status_code=500, detail=str(e))

