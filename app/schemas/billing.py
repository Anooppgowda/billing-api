from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


# =========================================================
# INVOICE ITEM SCHEMAS
# =========================================================

class InvoiceItemCreate(BaseModel):
    product_id: Optional[int] = Field(
        default=None,
        gt=0
    )

    description: str = Field(
        ...,
        min_length=1,
        max_length=255
    )

    quantity: int = Field(
        ...,
        gt=0
    )

    unit_price: Decimal = Field(
        ...,
        ge=0
    )

    tax_rate: Decimal = Field(
        default=Decimal("0.00"),
        ge=0,
        le=100
    )

    discount: Decimal = Field(
        default=Decimal("0.00"),
        ge=0
    )

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Description cannot be empty")

        return value


class InvoiceItemResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    invoice_id: int
    product_id: Optional[int] = None
    description: str
    quantity: int
    unit_price: Decimal
    tax_rate: Decimal
    discount: Decimal
    total_price: Decimal


# =========================================================
# INVOICE SCHEMAS
# =========================================================

class InvoiceCreate(BaseModel):
    customer_id: int = Field(
        ...,
        gt=0
    )

    items: list[InvoiceItemCreate] = Field(
        ...,
        min_length=1
    )

    due_date: Optional[date] = None

    discount_amount: Decimal = Field(
        default=Decimal("0.00"),
        ge=0
    )

    notes: Optional[str] = Field(
        default=None,
        max_length=1000
    )

    @field_validator("notes")
    @classmethod
    def validate_notes(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            value = value.strip()

            if not value:
                return None

        return value


class InvoiceUpdate(BaseModel):
    due_date: Optional[date] = None

    discount_amount: Optional[Decimal] = Field(
        default=None,
        ge=0
    )

    notes: Optional[str] = Field(
        default=None,
        max_length=1000
    )

    status: Optional[str] = None

    @field_validator("notes")
    @classmethod
    def validate_notes(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            value = value.strip()

            if not value:
                return None

        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            value = value.strip().upper()

            allowed_statuses = {
                "DRAFT",
                "ISSUED",
                "PAID",
                "CANCELLED"
            }

            if value not in allowed_statuses:
                raise ValueError(
                    "Status must be one of: "
                    "DRAFT, ISSUED, PAID, CANCELLED"
                )

        return value


class InvoiceResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    invoice_number: str
    customer_id: int

    subtotal: Decimal
    tax_amount: Decimal
    discount_amount: Decimal
    total_amount: Decimal

    status: str

    due_date: Optional[date] = None
    notes: Optional[str] = None

    created_at: datetime
    updated_at: datetime

    items: list[InvoiceItemResponse] = []


# =========================================================
# PAYMENT SCHEMAS
# =========================================================

class PaymentCreate(BaseModel):
    invoice_id: int = Field(
        ...,
        gt=0
    )

    amount: Decimal = Field(
        ...,
        gt=0
    )

    payment_method: str = Field(
        ...,
        min_length=1,
        max_length=50
    )

    @field_validator("payment_method")
    @classmethod
    def validate_payment_method(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Payment method cannot be empty")

        return value


class PaymentResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    invoice_id: int
    transaction_id: str

    amount: Decimal
    payment_method: str
    status: str

    paid_at: Optional[datetime] = None
    created_at: datetime