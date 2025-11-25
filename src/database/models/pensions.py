from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from src.database.models.database import Base

class Funds(Base):
    __tablename__ = "funds"
    fund_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    term = Column(String, nullable=False)
    waiting_time = Column(Integer, nullable=False)
    type = Column(String, nullable=False)
    active = Column(String, nullable=False)
    annual_return = Column(Float, nullable=False)

class Client(Base):
    __tablename__ = "client"
    client_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    available_balance = Column(Integer, nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(Integer, nullable=False)
    registration_date = Column(Date, nullable=False)
    document_type = Column(String, nullable=False)
    nu_document = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    status = Column(String, nullable=False)

class Subscriptions(Base):
    __tablename__ = "subscriptions"
    id_subscriptions = Column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )
    client_id = Column(Integer, ForeignKey("client.client_id"), nullable=False)
    fund_id = Column(Integer, ForeignKey("funds.fund_id"), nullable=False)
    start_date = Column(Date, nullable=False)
    amount = Column(Integer, nullable=False)

class Cancellations(Base):
    __tablename__ = "cancellations"
    cancelled_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    client_id = Column(Integer, ForeignKey("client.client_id"), nullable=False)
    fund_id = Column(Integer, ForeignKey("funds.fund_id"), nullable=False)
    id_subscriptions = Column(
        Integer, ForeignKey("subscriptions.id_subscriptions"), nullable=False
    )
    date_cancelled = Column(Date, nullable=False)
    start_amount = Column(Float, nullable=False)
    profit = Column(Float, nullable=False)

class Transactions(Base):
    __tablename__ = "transactions"
    transactions_id = Column(String, primary_key=True, nullable=False)
    id_subscriptions = Column(
        Integer, ForeignKey("subscriptions.id_subscriptions"), nullable=False
    )
    cancelled_id = Column(
        Integer, ForeignKey("cancellations.cancelled_id"), nullable=False
    )
    client_id = Column(Integer, ForeignKey("client.client_id"), nullable=False)
    fund_id = Column(Integer, ForeignKey("funds.fund_id"), nullable=False)
    date = Column(Date, nullable=False)
    type = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)

class Notifications(Base):
    __tablename__ = "notifications"
    id_notifications = Column(
        Integer, primary_key=True, autoincrement=True, nullable=False
    )
    client_id = Column(Integer, ForeignKey("client.client_id"), nullable=False)
    cancelled_id = Column(
        Integer, ForeignKey("cancellations.cancelled_id"), nullable=False
    )
    id_subscriptions = Column(
        Integer, ForeignKey("subscriptions.id_subscriptions"), nullable=False
    )
    sent_date = Column(Date, nullable=False)
    origin = Column(String, nullable=False)