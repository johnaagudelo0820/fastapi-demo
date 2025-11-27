from fastapi import FastAPI, HTTPException, status
from datetime import datetime
from zoneinfo import ZoneInfo

from db import create_all_tables
from models import Transaction, Invoice
from sqlmodel import select

from .routers import customers

# Create the FastAPI app instance
app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)

# Define the root endpoint
@app.get("/")
async def root():
    return {"message": "Hello, John!"}

country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}

@app.get("/time/{timezone}")
async def time(timezone: str):
    iso = timezone.upper()
    timezone_iso = country_timezones.get(iso)
    
    if not timezone_iso:
        return {"error": "Invalid timezone", "time": None}

    return {"time": datetime.now(ZoneInfo(timezone_iso))}


@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return invoice_data



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)