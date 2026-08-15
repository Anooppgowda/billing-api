from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class InvoiceItemCreate(BaseModel):
    product_id: Optional[int] = None

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


class InvoiceCreate(BaseModel):
    customer_id: int

    due_date: Optional[date] = None

    discount_amount: Decimal = Field(
        default=Decimal("0.00"),
        ge=0
    )

    notes: Optional[str] = None

    items: List[InvoiceItemCreate]


class InvoiceItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: Optional[int]
    description: str
    quantity: int
    unit_price: Decimal
    tax_rate: Decimal
    discount: Decimal
    total_price: Decimal


class InvoiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    invoice_number: str
    customer_id: int
    subtotal: Decimal
    tax_amount: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    status: str
    due_date: Optional[date]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    items: List[InvoiceItemResponse]
    
    
class PaymentCreate(BaseModel):
    invoice_id: int

    amount: Decimal = Field(
        ...,
        gt=0
    )

    payment_method: str


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    invoice_id: int
    transaction_id: str
    amount: Decimal
    payment_method: str
    status: str
    paid_at: Optional[datetime]
    created_at: datetime