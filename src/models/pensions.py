from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from models.database import Base

class Funds(Base):
    __tablename__="Funds"
    FundId= Column( Integer, primary_key=True, index=True,  autoincrement=True)
    Name= Column(String, nullable= False)
    Term= Column(String, nullable= False)
    WaitingTime= Column(Integer, nullable= False)
    Type= Column(String, nullable= False)
    Active = Column(Integer, nullable = False)
    Annual_return= Column(Float, nullable=False)

class Client(Base):
    __tablename__="Client"
    ClientId = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    FirtName = Column(String, nullable=False)
    LastName = Column (String, nullable=False)
    AvailableBalance = Column(Integer, nullable=False)
    Email = Column(String, nullable=False)
    PhoneNumber = Column(Integer, nullable=False)
    RegistrationDate = Column(Date, nullable=False)
    DocumentType = Column(String, nullable=False)
    NuDocument  = Column(Integer, nullable=False)
    Gender= Column(String, nullable=False)
    Status = Column(String, nullable=False)

class Subscriptions(Base):
    __tablename__="Subscriptions"
    IdSubscriptions = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    ClientId = Column(Integer, ForeignKey("Client.ClientId"), nullable=False)
    FundId = Column(Integer, ForeignKey("Funds.FundId"), nullable=False)
    StartDate = Column(Date, nullable=False)
    Amount= Column(Integer,nullable=False)

class Cancellations(Base):
    __tablename__="Cancellations"
    CancelledId = Column(Integer, primary_key=True,  autoincrement=True,  nullable=False)
    ClientId = Column(Integer, ForeignKey("Client.ClientId"), nullable=False)
    FundId = Column(Integer, ForeignKey("Funds.FundId"), nullable=False)
    IdSubscriptions = Column(Integer,ForeignKey("Subscriptions.IdSubscriptions"), nullable=False)
    DateCancelled = Column(Date, nullable=False)
    StartAmount = Column(Float,nullable=False)
    Profit = Column(Float,nullable=False)

class Transactions(Base):
    __tablename__ = "Transactions" 

    TransactionsId = Column(String, primary_key=True,  nullable=False)
    IdSubscriptions = Column(Integer, ForeignKey("Subscriptions.IdSubscriptions"), nullable=False)
    CancelledId = Column(Integer, ForeignKey("Cancellations.CancelledId"), nullable=False)
    ClientId = Column(Integer, ForeignKey("Client.ClientId"), nullable=False)
    FundId = Column(Integer, ForeignKey("Funds.FundId"), nullable=False)
    Date = Column(Date,  nullable=False)
    Type = Column(String, nullable=False)
    Amount = Column(Integer,nullable=False)

class Notifications(Base):
    __tablename__ = "Notifications"
    IdNotifications  = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    ClientId = Column(Integer, ForeignKey("Client.ClientId"), nullable=False)
    CancelledId= Column(Integer, ForeignKey("Cancellations.CancelledId"), nullable=False)
    IdSubscriptions = Column(Integer, ForeignKey("Subscriptions.IdSubscriptions"), nullable=False)
    SentDate = Column(Date,  nullable=False)
    Origin = Column(String,  nullable=False)



