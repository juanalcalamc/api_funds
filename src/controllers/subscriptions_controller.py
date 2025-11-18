import uuid
import datetime
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from models.pensions import subscriptions, transactions
from schemas.dto import SubscriptionOut, SubscriptionsCreate
from models.database import get_db
from utils.notifications import Email, SMS, NotificationContext
from utils.logging import logger


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
    subscribe = subscriptions(
        client_id=payload.client_id,
        fund_id=payload.fund_id,
        start_date=payload.start_date,
        amount=payload.amount,
    )

    db.add(subscribe)
    db.commit()
    db.refresh(subscribe)

    Transaction = transactions(
        transactions_id=str(uuid.uuid4()),
        id_subscriptions=subscribe.id_subscriptions,
        cancelled_id=0,
        client_id=subscribe.client_id,
        fund_id=subscribe.fund_id,
        date=datetime.datetime.now(),
        type="subscription",
        amount=payload.amount,
    )
    db.add(Transaction)
    db.commit()
    db.refresh(Transaction)

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
        "message": "Subscription created and transaction recorded",
        "subscription": subscribe,
        "transaction": Transaction,
    }


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
def delete_subscription(subscriptionsid: int, db: Session = Depends(get_db)):
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

    subscription = (
        db.query(subscriptions)
        .filter(subscriptions.id_subscriptions == subscriptionsid)
        .first()
    )
    if not subscription:
        logger.error(f"Subscriptions with ID {subscriptionsid} not found.")
        raise HTTPException(status_code=404, detail="Subscription not found")

    db.delete(subscription)
    db.commit()
    return None
