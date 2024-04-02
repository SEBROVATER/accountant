from datetime import datetime
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Form, Request, status

from app.expenses.models import Currency, Expense
from app.routes import templates

router = APIRouter()


@router.get("/expenses/table")
async def get_expenses_table(request: Request):
    expenses = await Expense.all().order_by("-date").all()
    return templates.TemplateResponse(
        request, "expenses/tbody.html", context={"expenses": expenses}
    )


@router.get("/expenses/")
async def get_expenses(request: Request):
    expenses = await Expense.all().order_by("-date").all()
    return templates.TemplateResponse(
        request,
        "expenses/main.html",
        context={
            "expenses": expenses,
        },
    )


@router.post("/expenses/")
async def save(
    request: Request,
    name: Annotated[str, Form()],
    amount: Annotated[Decimal, Form()],
    currency: Annotated[Currency, Form()],
    count: Annotated[Decimal, Form()],
    date: Annotated[datetime, Form()],
):
    obj = await Expense.create(name=name, amount=amount, currency=currency, count=count, date=date)
    print(obj)
    resp = templates.TemplateResponse(
        request,
        "expenses/save_response.html",
        context={
            "expense": obj,
            "text": f"New expense {obj.id} added",
            "alert_class": "ok",
        },
        status_code=status.HTTP_201_CREATED,
    )
    resp.headers["HX-Trigger"] = "newExpense"
    return resp


@router.delete("/expenses/{expense_id}")
async def delete_expense(request: Request, expense_id: int):
    try:
        print(f"delete {expense_id}")
        obj = await Expense.filter(id=expense_id).delete()
        print(obj)
        return templates.TemplateResponse(
            request,
            "shared/alert.html",
            context={"text": f"{expense_id} removed", "alert_class": "ok"},
            status_code=status.HTTP_200_OK,
        )
    except Exception as exc:
        print(exc)
        raise exc
