from datetime import datetime


from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Numeric,
    ForeignKey,
    Enum,
)

from sqlalchemy.orm import relationship

from app.db.database import Base


class Payment(Base):
    __tablename__ = "payments"

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

    transaction_id = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    payment_method = Column(
        Enum(
            "CASH",
            "CARD",
            "UPI",
            "BANK_TRANSFER",
            "ONLINE",
            name="payment_method"
        ),
        nullable=False
    )

    status = Column(
        Enum(
            "PENDING",
            "SUCCESS",
            "FAILED",
            "REFUNDED",
            name="payment_status"
        ),
        nullable=False,
        default="PENDING"
    )

    paid_at = Column(
        DateTime,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    invoice = relationship(
        "Invoice",
        back_populates="payments"
    )