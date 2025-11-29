from fastapi import APIRouter, status
from models import Plan
from db import Sessiondep
from sqlmodel import select

router = APIRouter()

@router.post("/plans", tags=["plans"], status_code=status.HTTP_201_CREATED)
async def create_plan(plan_data: Plan, session: Sessiondep):
    plan_db = Plan.model_validate(plan_data.model_dump())
    session.add(plan_db)
    session.commit()
    session.refresh(plan_db)
    return plan_db

@router.get("/plans", tags=["plans"], response_model=list[Plan])
async def get_plans(session: Sessiondep):
    query = select(Plan)
    result = session.exec(query).all()
    return result