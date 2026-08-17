from decimal import Decimal

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Numeric,
)

from sqlalchemy.orm import relationship

from app.db.database import Base


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    invoice_id = Column(
        Integer,
        ForeignKey("invoices.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    product_id = Column(
        Integer,
        nullable=True,
        index=True
    )

    description = Column(
        String(255),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False,
        default=1
    )

    unit_price = Column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00")
    )

    tax_rate = Column(
        Numeric(5, 2),
        nullable=False,
        default=Decimal("0.00")
    )

    discount = Column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00")
    )

    total_price = Column(
        Numeric(12, 2),
        nullable=False,
        default=Decimal("0.00")
    )

    invoice = relationship(
        "Invoice",
        back_populates="items"
    )