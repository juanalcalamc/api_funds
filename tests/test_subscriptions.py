import pytest
from datetime import date
from src.models.pensions import  funds, subscriptions
from src.controllers import subscriptions_controller
from src.models.database import Base, engine, SessionLocal

@pytest.fixture
def db_session():
    # Crear todas las tablas en la base de datos de pruebas
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Opcional: limpiar las tablas después de cada test
        Base.metadata.drop_all(bind=engine)
@pytest.fixture
def payload():
    from src.schemas.dto import SubscriptionsCreate
    return SubscriptionsCreate(
        client_id = 1,
        fund_id = 1,
        amount = 1000.0,
        start_date = date(2025, 11, 11),
        notification = "sms"
    )
def test_create_subscription(db_session, payload):
    fund = funds(
        fund_id=1,
        name="Test Fund",
        term="10 años",
        waiting_time=5,
        type="Retirement",
        active=True,
        annual_return=0.05,
    )
    db_session.add(fund)
    db_session.commit()
    response = subscriptions_controller.created_subscribe(payload, db_session)
    sub = response["subscription"]

    assert sub.id_subscriptions is not None
    assert sub.client_id == payload.client_id
    assert sub.fund_id == fund.fund_id
    assert sub.amount == payload.amount
    assert sub.start_date == payload.start_date
 