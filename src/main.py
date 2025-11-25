from fastapi import FastAPI
from src.controllers import (cancellations_controller,subscriptions_controller,funds_controller,transactions_controller,
)
from src.database.models.database import engine
from src.database.models.pensions import Base
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Pension Fund API",
    version="1.0.0",
    description="API for managing pension fund subscriptions and transactions.",
)
app.include_router(
    subscriptions_controller.router, prefix="/api/funds", tags=["Subscriptions"]
)
app.include_router(
    cancellations_controller.router, prefix="/api/funds", tags=["Cancellations"]
)
app.include_router(
    transactions_controller.router, prefix="/api/funds", tags=["Transactions"]
)
app.include_router(funds_controller.router, prefix="/api/funds", tags=["funds"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)