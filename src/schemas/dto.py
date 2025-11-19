from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# CModelos de Suscripciones
class SubscriptionBase(BaseModel):
    client_id: int
    fund_id: int
    amount: float
    start_date: datetime
    notification: Optional[str] = None

class SubscriptionsCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(SubscriptionBase):
    client_id: Optional[int] = None
    fund_id: Optional[int] = None
    amount: Optional[float] = None
    start_date: Optional[datetime] = None
    notification: Optional[str] = None

class SubscriptionOut(SubscriptionBase):
    id_subscriptions: int

    class Config:
        from_attributes = True

# Modelous de caclacion
class CancelBase(BaseModel):
    client_id: int
    fund_id: int
    id_subscriptions: int
    start_amount: float
    profit: float
    notification: Optional[str] = None

class CancelCreate(CancelBase):
    pass

class CancelUpdate(CancelBase):
    client_id: Optional[int] = None
    fund_id: Optional[int] = None
    id_subscriptions: Optional[int] = None
    start_amount: Optional[float] = None
    profit: Optional[float] = None

class CancelOut(CancelBase):
    cancelled_id: int

    class Config:
        from_attributes = True

# Mdelos transacciones
class TransactionBase(BaseModel):
    transactions_id: str
    id_subscriptions: int
    cancelled_id: int
    client_id: int
    fund_id: int
    date: datetime
    type: str
    amount: int

class TransactionCreate(TransactionBase):
    pass

class TransactionsOut(TransactionBase):
    transactions_id: str

    class Config:
        from_attributes = True

# Modelos de los fondos
class FundBase(BaseModel):
    name: str
    term: str
    waiting_time: int
    type: str
    active: int
    annual_return: float

class FundCreate(FundBase):
    pass

class FundUpdate(BaseModel):
    name: Optional[str] = None
    term: Optional[str] = None
    waiting_time: Optional[int] = None
    type: Optional[str] = None
    active: Optional[int] = None
    annual_return: Optional[float] = None

class FundOut(FundBase):
    fund_id: int

    class Config:
        from_attributes = True

#Notification 
class NotificationBase(BaseModel):
    client_id: int
    cancelled_id: int
    id_subscriptions: int
    sent_date: datetime
    origin: str

class NotificationCreate(NotificationBase):
    pass