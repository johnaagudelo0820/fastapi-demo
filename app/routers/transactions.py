from fastapi import APIRouter, HTTPException, status
from models import Transaction, TransactionCreate, Customer
from db import Sessiondep
from sqlmodel import select

router = APIRouter()

@router.post("/transactions", tags=["transactions"], status_code=status.HTTP_201_CREATED)
async def create_transaction(transaction_data: TransactionCreate, session: Sessiondep):
    transaction_data_dict = transaction_data.model_dump()
    customer: Customer = session.get(Customer, transaction_data_dict.get("customer_id"))
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    
    transaction_db = Transaction.model_validate(transaction_data_dict)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)

    return transaction_db

@router.get("/transactions", tags=["transactions"], response_model=list[Transaction])
async def list_transaction(session: Sessiondep):
    query = select(Transaction)
    result = session.exec(query).all()
    return result