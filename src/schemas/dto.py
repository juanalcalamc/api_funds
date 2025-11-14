from pydantic import BaseModel
from typing import Optional
from datetime import datetime

#CModelos de Suscripciones
class SubscriptionBase(BaseModel):
    ClientId: int
    FundId: int
    Amount: float
    StartDate: datetime
    Notification: Optional[str] = None

class SubscriptionsCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(SubscriptionBase):
    ClientId: Optional[int] = None
    FundId: Optional[int] = None
    Amount: Optional[float] = None
    StartDate: Optional[datetime] = None
    Notification: Optional[str] = None

class SubscriptionOut(SubscriptionBase):
    IdSubscriptions : int
    class Config:
        from_attributes = True 


#Modelous de caclacion
class CancelBase(BaseModel):
    ClientId: int
    FundId: int
    IdSubscriptions: int
    StartAmount: float
    Profit: float


class CancelCreate(CancelBase):
   pass

class CancelUpdate(CancelBase):
    ClientId: Optional[int] = None  
    FundId: Optional[int] = None  
    IdSubscriptions: Optional[int] = None  
    StartAmount: Optional[float] = None  
    Profit: Optional[float] = None 
   

class CancelOut(CancelBase):
    CancelledId : int
    class Config:
        from_attributes = True 

#Mdelos transacciones
class TransactionBase(BaseModel):
    TransactionsId : str
    IdSubscriptions : int
    CancelledId : int
    ClientId : int
    FundId : int
    Date : datetime
    Type : str
    Amount : int

class TransactionCreate(TransactionBase):
    pass

# class TransactionsUpdate(TransactionBase):
#     Type: Optional[str] = None  
#     FundId: Optional[int] = None
#     Date: Optional[datetime] = None
#     Amount: Optional[float] = None

class TransactionsOut(TransactionBase):
    TransactionsId: str

    class Config:
        from_attributes = True 


#Modelos de los fondos 

class FundBase(BaseModel):
    Name: str
    Term: str
    WaitingTime: int
    Type: str
    Active: int
    Annual_return: float

class FundCreate(FundBase):
    pass

class FundUpdate(BaseModel):
    Name: Optional[str] = None
    Term: Optional[str] = None
    WaitingTime: Optional[int] = None
    Type: Optional[str] = None
    Active: Optional[int] = None
    Annual_return: Optional[float] = None

class FundOut(FundBase):
    FundId: int

    class Config:
        from_attributes = True 