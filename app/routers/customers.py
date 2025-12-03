from models import StatusEnum
from models import CustomerPlan
from fastapi import APIRouter, HTTPException, status, Query

from models import Customer, CustomerCreate, CustomerUpdate, StatusEnum
from db import Sessiondep

from sqlmodel import select


router = APIRouter()


@router.post("/customers", response_model=Customer, tags=["customers"])
async def create_customer(customer_data: CustomerCreate, session: Sessiondep):
    customer = Customer.model_validate(customer_data.model_dump()) # Convert the CustomerCreate model to a Customer model
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@router.get("/customers/{customer_id}", response_model=Customer, tags=["customers"])
async def read_customer(customer_id: int, session: Sessiondep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer_db

@router.patch("/customers/{cusomer_id}", response_model=Customer, status_code=status.HTTP_201_CREATED, tags=["customers"])
async def update_customer(customer_id: int, customer_data: CustomerUpdate, session: Sessiondep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    customer_data_dict = customer_data.model_dump(exclude_unset=True) # convert the CustomerUpdate model to a dictionary
    customer_db.sqlmodel_update(customer_data_dict) # update the customer
    session.add(customer_db) # add the customer to the session
    session.commit() # commit the session
    session.refresh(customer_db) # refresh the customer
    return customer_db

@router.delete("/customers/{customer_id}", response_model=Customer, tags=["customers"])
async def delete_customer(customer_id: int, session: Sessiondep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    session.delete(customer_db)
    session.commit()
    return {"detail": "Customer deleted successfully"}

@router.get("/customers", response_model=list[Customer], tags=["customers"])
async def get_customers(session: Sessiondep):
    return session.exec(select(Customer)).all()

@router.post("/customers/{customer_id}/plans/{plan_id}", tags=["customers"])
async def suscribe_customer_to_plan(
    customer_id: int, plan_id: int, session: Sessiondep,
    plan_status: StatusEnum = Query(),
):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    plan_db = session.get(Plan, plan_id)
    if not plan_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found")
    
    customer_plan_db = CustomerPlan(
        plan_id=plan_db.id, customer_id=customer_db.id, status=plan_status
    )
    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db)

    return customer_plan_db


@router.get("/customers/{customer_id}/plans", tags=["customers"])
async def suscribe_customer_to_plan(
    customer_id: int, session: Sessiondep, plan_status: StatusEnum = Query()
):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    query = select(CustomerPlan).where(CustomerPlan.customer_id == customer_id).where(CustomerPlan.status == plan_status)
    plans = session.exec(query).all()
    return plans