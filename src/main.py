from fastapi import FastAPI
from controllers import (
    cancellations_controller,
    subscriptions_controller,
    funds_controller,
    transactions_controller,
)
from models.database import engine
from models.pensions import Base

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Pension Fund API",
    version="1.0.0",
    description="API for managing pension fund subscriptions and transactions.",
)

app.include_router(
    subscriptions_controller.router, prefix="/funds", tags=["Subscriptions"]
)
app.include_router(
    cancellations_controller.router, prefix="/funds", tags=["Cancellations"]
)
app.include_router(
    transactions_controller.router, prefix="/funds", tags=["Transactions"]
)
app.include_router(funds_controller.router, prefix="/funds", tags=["Funds"])
