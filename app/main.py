from fastapi import FastAPI, HTTPException, status, Request
from datetime import datetime
from zoneinfo import ZoneInfo
import time

from db import create_all_tables
from sqlmodel import select

from .routers import customers, transactions, invoices, plans

# Create the FastAPI app instance
app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(invoices.router)
app.include_router(plans.router)

@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request: {request.method} {request.url} completed in {process_time:.4f} seconds")
    return response

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
async def time_by_timezone(timezone: str):
    iso = timezone.upper()
    timezone_iso = country_timezones.get(iso)
    
    if not timezone_iso:
        return {"error": "Invalid timezone", "time": None}

    return {"time": datetime.now(ZoneInfo(timezone_iso))}




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)