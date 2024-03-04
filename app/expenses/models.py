from decimal import Decimal
from enum import Enum

from tortoise.fields import (
    CharEnumField,
    DatetimeField,
    DecimalField,
    TextField,
)
from tortoise.models import Model


class Currency(str, Enum):
    USD = "USD"
    KGS = "KGS"
    RUB = "RUB"
    TRY = "TRY"
    EUR = "EUR"


class TimestampMixin:
    created_at = DatetimeField(auto_now_add=True, null=False)
    updated_at = DatetimeField(auto_now=True, null=False)


class Expense(TimestampMixin, Model):
    name = TextField(null=False)
    amount: Decimal = DecimalField(max_digits=20, decimal_places=10, null=False)
    currency: Currency = CharEnumField(Currency, max_length=5, null=False)
    count: Decimal = DecimalField(
        max_digits=20, decimal_places=10, null=False, default=Decimal(1.0)
    )

    date = DatetimeField(auto_now_add=True)

    def __str__(self) -> str:
        name = self.name
        if len(name) > 7:
            name = f"{name[:7]}..."
        return f"{name} ({self.amount}{self.currency})"
