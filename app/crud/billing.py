from decimal import Decimal
from uuid import uuid4

from sqlalchemy.orm import Session, joinedload

from app.models.billing import Invoice
from app.models.invoice_item import InvoiceItem
from app.models.payment import Payment
from app.models.customer import Customer


# =========================================================
# INVOICE NUMBER GENERATOR
# =========================================================

def generate_invoice_number() -> str:
    """
    Generate a unique invoice number.
    Example: INV-20260815-A1B2C3
    """
    return f"INV-{uuid4().hex[:10].upper()}"


# =========================================================
# CALCULATE INVOICE TOTALS
# =========================================================

def calculate_invoice_totals(items):
    """
    Calculate subtotal, tax and total amount.
    """

    subtotal = Decimal("0.00")
    tax_amount = Decimal("0.00")

    for item in items:
        item_subtotal = (
            Decimal(item.quantity) *
            Decimal(item.unit_price)
        )

        discount = Decimal(item.discount or 0)

        taxable_amount = item_subtotal - discount

        if taxable_amount < 0:
            taxable_amount = Decimal("0.00")

        tax = (
            taxable_amount *
            Decimal(item.tax_rate or 0) /
            Decimal("100")
        )

        item.total_price = taxable_amount + tax

        subtotal += item_subtotal
        tax_amount += tax

    return subtotal, tax_amount


# =========================================================
# CREATE INVOICE
# =========================================================

def create_invoice(
    db: Session,
    customer_id: int,
    items_data,
    due_date=None,
    discount_amount=Decimal("0.00"),
    notes=None,
):
    """
    Create an invoice with invoice items.
    """

    # Check customer
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        return None

    # Create invoice
    invoice = Invoice(
        invoice_number=generate_invoice_number(),
        customer_id=customer_id,
        due_date=due_date,
        discount_amount=Decimal(discount_amount),
        notes=notes,
        status="DRAFT",
    )

    db.add(invoice)
    db.flush()

    # Create invoice items
    for item_data in items_data:

        item = InvoiceItem(
            invoice_id=invoice.id,
            product_id=item_data.product_id,
            description=item_data.description,
            quantity=item_data.quantity,
            unit_price=Decimal(item_data.unit_price),
            tax_rate=Decimal(item_data.tax_rate),
            discount=Decimal(item_data.discount),
        )

        db.add(item)

    db.flush()

    # Calculate totals
    subtotal, tax_amount = calculate_invoice_totals(
        invoice.items
    )

    invoice.subtotal = subtotal
    invoice.tax_amount = tax_amount

    invoice.total_amount = (
        subtotal
        + tax_amount
        - Decimal(discount_amount)
    )

    if invoice.total_amount < 0:
        invoice.total_amount = Decimal("0.00")

    db.commit()

    db.refresh(invoice)

    return invoice


# =========================================================
# GET INVOICE BY ID
# =========================================================

def get_invoice(
    db: Session,
    invoice_id: int
):
    return (
        db.query(Invoice)
        .options(
            joinedload(Invoice.items),
            joinedload(Invoice.payments),
        )
        .filter(Invoice.id == invoice_id)
        .first()
    )


# =========================================================
# GET ALL INVOICES
# =========================================================

def get_invoices(
    db: Session,
    skip: int = 0,
    limit: int = 100,
):
    return (
        db.query(Invoice)
        .options(
            joinedload(Invoice.items)
        )
        .order_by(Invoice.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


# =========================================================
# UPDATE INVOICE
# =========================================================

def update_invoice(
    db: Session,
    invoice_id: int,
    due_date=None,
    discount_amount=None,
    notes=None,
    status=None,
):
    invoice = (
        db.query(Invoice)
        .filter(Invoice.id == invoice_id)
        .first()
    )

    if not invoice:
        return None

    if due_date is not None:
        invoice.due_date = due_date

    if discount_amount is not None:
        invoice.discount_amount = Decimal(
            discount_amount
        )

        invoice.total_amount = (
            invoice.subtotal
            + invoice.tax_amount
            - invoice.discount_amount
        )

        if invoice.total_amount < 0:
            invoice.total_amount = Decimal("0.00")

    if notes is not None:
        invoice.notes = notes

    if status is not None:
        invoice.status = status

    db.commit()
    db.refresh(invoice)

    return invoice


# =========================================================
# DELETE / CANCEL INVOICE
# =========================================================

def cancel_invoice(
    db: Session,
    invoice_id: int
):
    invoice = (
        db.query(Invoice)
        .filter(Invoice.id == invoice_id)
        .first()
    )

    if not invoice:
        return None

    invoice.status = "CANCELLED"

    db.commit()
    db.refresh(invoice)

    return invoice


# =========================================================
# CREATE PAYMENT
# =========================================================

def create_payment(
    db: Session,
    invoice_id: int,
    amount,
    payment_method: str,
):
    """
    Create a payment for an invoice.
    """

    invoice = (
        db.query(Invoice)
        .filter(Invoice.id == invoice_id)
        .first()
    )

    if not invoice:
        return None

    amount = Decimal(amount)

    if amount <= 0:
        raise ValueError(
            "Payment amount must be greater than zero"
        )

    if invoice.status == "CANCELLED":
        raise ValueError(
            "Cannot make payment for a cancelled invoice"
        )

    # Calculate already paid amount
    paid_amount = (
        db.query(Payment)
        .filter(
            Payment.invoice_id == invoice_id,
            Payment.status == "SUCCESS",
        )
        .with_entities(Payment.amount)
        .all()
    )

    total_paid = sum(
        (Decimal(row[0]) for row in paid_amount),
        Decimal("0.00")
    )

    remaining_amount = (
        Decimal(invoice.total_amount)
        - total_paid
    )

    if amount > remaining_amount:
        raise ValueError(
            f"Payment exceeds remaining amount "
            f"({remaining_amount})"
        )

    payment = Payment(
        invoice_id=invoice_id,
        transaction_id=f"TXN-{uuid4().hex[:12].upper()}",
        amount=amount,
        payment_method=payment_method,
        status="SUCCESS",
    )

    db.add(payment)

    # Update invoice status
    if amount == remaining_amount:
        invoice.status = "PAID"
    else:
        invoice.status = "ISSUED"

    db.commit()

    db.refresh(payment)

    return payment


# =========================================================
# GET PAYMENT BY ID
# =========================================================

def get_payment(
    db: Session,
    payment_id: int
):
    return (
        db.query(Payment)
        .filter(Payment.id == payment_id)
        .first()
    )


# =========================================================
# GET PAYMENTS FOR INVOICE
# =========================================================

def get_invoice_payments(
    db: Session,
    invoice_id: int
):
    return (
        db.query(Payment)
        .filter(Payment.invoice_id == invoice_id)
        .order_by(Payment.id.desc())
        .all()
    )