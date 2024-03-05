from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Request
from tortoise.functions import Sum

from app.expenses.models import Expense
from app.routes import templates

router = APIRouter()


@router.get("/dashboards/")
async def get_dashboards(request: Request):
    now = datetime.now(UTC)

    totals_month = dict()
    for data in (
        await Expense.filter(date__gt=now - timedelta(days=31))
        .annotate(total=Sum("amount"))
        .group_by("currency")
        .values("currency", "total")
    ):
        totals_month[data["currency"]] = data["total"]
    totals_year = dict()
    for data in (
        await Expense.filter(date__gt=now - timedelta(days=365))
        .annotate(total=Sum("amount"))
        .group_by("currency")
        .values("currency", "total")
    ):
        totals_year[data["currency"]] = data["total"]
    totals_overall = dict()
    for data in (
        await Expense.annotate(total=Sum("amount")).group_by("currency").values("currency", "total")
    ):
        totals_overall[data["currency"]] = data["total"]

    relevant_currencies = await Expense.all().distinct().values_list("currency", flat=True)
    return templates.TemplateResponse(
        request,
        "dashboards/main.html",
        context={
            "relevant_currencies": relevant_currencies,
            "totals_month": totals_month,
            "totals_year": totals_year,
            "totals_overall": totals_overall,
        },
    )
