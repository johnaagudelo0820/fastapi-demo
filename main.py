from fastapi import FastAPI, HTTPException, status
from datetime import datetime
from zoneinfo import ZoneInfo

from models import Transaction, Invoice, CustomerCreate, Customer
from db import Sessiondep, create_all_tables
from sqlmodel import select

# Create the FastAPI app instance
app = FastAPI(lifespan=create_all_tables)

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

# Simulate the database id
db_customers: list[Customer] = []

@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: Sessiondep):
    customer = Customer.model_validate(customer_data.model_dump()) # Convert the CustomerCreate model to a Customer model
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@app.get("/customers/{customer_id}", response_model=Customer)
async def read_customer(customer_id: int, session: Sessiondep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    
    return customer_db

@app.get("/customers", response_model=list[Customer])
async def get_customers(session: Sessiondep):
    return session.exec(select(Customer)).all()

@app.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int):
    customer = next((customer for customer in db_customers if customer.id == customer_id), None) # fucntion getenerator to find the customer
    if not customer:
        return {"error": "Customer not found", "customer": None}
    return customer

@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return invoice_data



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)