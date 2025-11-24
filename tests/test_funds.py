import pytest
from fastapi import HTTPException
from src.models.pensions import funds
from src.controllers import funds_controller
from src.models.database import Base, engine, SessionLocal
from src.schemas.dto import FundUpdate,FundCreate,FundOut

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
@pytest.fixture
def payload():
    return FundCreate(
        name="Test Fund",
        term="10 años",
        waiting_time=5,
        type="Retirement",
        active=True,
        annual_return=7.5
    )
def test_create_funds(payload, db_session):
    fund = funds_controller.create_fund(payload, db_session)
    
    assert fund.name == payload.name
    assert fund.term == payload.term
    assert fund.waiting_time == payload.waiting_time
    assert fund.type == payload.type
    assert fund.active == payload.active
    assert fund.annual_return == payload.annual_return

def test_update_fund(payload, db_session):
    
    created_fund = funds_controller.create_fund(payload, db_session)
    fund_id = created_fund.fund_id

    update_payload = FundUpdate(
        name="Updated Fund",
        term="12 años",
        waiting_time=6,
        type="Retirement",
        active=False,
        annual_return=8.0
    )

    fund = funds_controller.update_fund(fund_id, update_payload, db_session)

    assert fund.name == "Updated Fund"
    assert fund.term == "12 años"
    assert fund.waiting_time == 6
    assert fund.type == "Retirement"
    assert fund.active == False
    assert fund.annual_return == 8.0

def test_delete_fund(payload, db_session):
    created_fund = funds_controller.create_fund(payload, db_session)
    fund_id = created_fund.fund_id

    response = funds_controller.delete_fund(fund_id, db_session)
    assert response["message"] == "Fund deleted successfully"

    
    with pytest.raises(HTTPException):
        funds_controller.get_fund(fund_id, db_session)