from datetime import datetime
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Form, Request, status

from app.expenses.models import Currency, Expense
from app.routes import templates

router = APIRouter()


@router.get("/expenses/")
async def get_expenses(request: Request):
    expenses = await Expense.all()
    return templates.TemplateResponse(request, "expenses/main.html", context={"expenses": expenses})


@router.post("/expenses/")
async def save(
    request: Request,
    name: Annotated[str, Form()],
    amount: Annotated[Decimal, Form()],
    currency: Annotated[Currency, Form()],
    count: Annotated[Decimal, Form()],
    date: Annotated[datetime, Form()],
):
    await Expense.create(name=name, amount=amount, currency=currency, count=count, date=date)

    return templates.TemplateResponse(
        request,
        "/shared/notification.html",
        context={"notificaton_class_": "ok", "text": "New expense added"},
        status_code=status.HTTP_201_CREATED,
    )
