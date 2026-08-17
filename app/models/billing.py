from datetime import datetime, date
from decimal import Decimal

from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    Numeric,
    ForeignKey,
    Enum,
    Text,
)
from sqlalchemy.orm import relationship

from app.db.database import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)

    invoice_number = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False,
        index=True
    )

    subtotal = Column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00")
    )

    tax_amount = Column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00")
    )

    discount_amount = Column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00")
    )

    total_amount = Column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00")
    )

    status = Column(
        Enum(
            "DRAFT",
            "ISSUED",
            "PAID",
            "CANCELLED",
            name="invoice_status"
        ),
        nullable=False,
        default="DRAFT"
    )

    due_date = Column(Date, nullable=True)

    notes = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # Relationships
    items = relationship(
        "InvoiceItem",
        back_populates="invoice",
        cascade="all, delete-orphan"
    )

    payments = relationship(
        "Payment",
        back_populates="invoice",
        cascade="all, delete-orphan"
    )