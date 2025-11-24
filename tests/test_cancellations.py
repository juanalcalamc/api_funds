import pytest
from datetime import date
from src.models.database import Base, engine, SessionLocal
from src.controllers import  cancellations_controller
from src.models.pensions import cancellations
from src.schemas.dto import CancelCreate, CancelOut

@pytest.fixture
def db_session():
    # Crear todas las tablas en la base de datos de pruebas
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
       
@pytest.fixture
def payload():
    
    return CancelCreate(
            client_id = 1,
            fund_id = 1,
            id_subscriptions = 1,
            start_amount = 0,
            profit = 0,
            )
def test_create_cancellation(payload, db_session):
    from src.models.pensions import subscriptions, funds
    sub = subscriptions(
        client_id=1,
        fund_id=1,
        amount=1000.0,
        start_date=date(2023, 1, 1),
    )
    fund = funds(
        name="Test Fund",
        term="10 años",
        waiting_time=5,
        type="Retirement",
        active=True,
        annual_return=0.05,
    )
    db_session.add(sub)
    db_session.add(fund)
    db_session.commit()
 
    response = cancellations_controller.create_cancellation(db_session, payload)
    canceled = response["cancellations"]

    assert canceled.client_id == sub.client_id
    assert canceled.fund_id == fund.fund_id
    assert canceled.id_subscriptions == sub.id_subscriptions
    assert canceled.start_amount == sub.amount
    assert canceled.profit == fund.annual_return * sub.amount