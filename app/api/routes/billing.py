from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.crud.billing import (
    create_invoice,
    get_invoice,
    get_invoices,
    update_invoice,
    cancel_invoice,
    create_payment,
    get_payment,
    get_invoice_payments,
)

from app.schemas.billing import (
    InvoiceCreate,
    InvoiceResponse,
    InvoiceUpdate,
    PaymentCreate,
    PaymentResponse,
)


router = APIRouter(
    prefix="/billing",
    tags=["Billing"]
)


# =========================================================
# CREATE INVOICE
# =========================================================

@router.post(
    "/invoices",
    response_model=InvoiceResponse,
    status_code=status.HTTP_201_CREATED
)
def create_invoice_api(
    invoice_data: InvoiceCreate,
    db: Session = Depends(get_db)
):
    invoice = create_invoice(
        db=db,
        customer_id=invoice_data.customer_id,
        items_data=invoice_data.items,
        due_date=invoice_data.due_date,
        discount_amount=invoice_data.discount_amount,
        notes=invoice_data.notes,
    )

    if invoice is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return invoice


# =========================================================
# GET ALL INVOICES
# =========================================================

@router.get(
    "/invoices",
    response_model=list[InvoiceResponse]
)
def get_all_invoices(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_invoices(
        db=db,
        skip=skip,
        limit=limit
    )


# =========================================================
# GET INVOICE BY ID
# =========================================================

@router.get(
    "/invoices/{invoice_id}",
    response_model=InvoiceResponse
)
def get_invoice_api(
    invoice_id: int,
    db: Session = Depends(get_db)
):
    invoice = get_invoice(
        db=db,
        invoice_id=invoice_id
    )

    if invoice is None:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    return invoice


# =========================================================
# UPDATE INVOICE
# =========================================================

@router.put(
    "/invoices/{invoice_id}",
    response_model=InvoiceResponse
)
def update_invoice_api(
    invoice_id: int,
    invoice_data: InvoiceUpdate,
    db: Session = Depends(get_db)
):
    invoice = update_invoice(
        db=db,
        invoice_id=invoice_id,
        due_date=invoice_data.due_date,
        discount_amount=invoice_data.discount_amount,
        notes=invoice_data.notes,
        status=invoice_data.status,
    )

    if invoice is None:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    return invoice


# =========================================================
# CANCEL INVOICE
# =========================================================

@router.delete(
    "/invoices/{invoice_id}",
    response_model=InvoiceResponse
)
def cancel_invoice_api(
    invoice_id: int,
    db: Session = Depends(get_db)
):
    invoice = cancel_invoice(
        db=db,
        invoice_id=invoice_id
    )

    if invoice is None:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    return invoice


# =========================================================
# CREATE PAYMENT
# =========================================================

@router.post(
    "/payments",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_payment_api(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db)
):
    try:

        payment = create_payment(
            db=db,
            invoice_id=payment_data.invoice_id,
            amount=payment_data.amount,
            payment_method=payment_data.payment_method,
        )

        if payment is None:
            raise HTTPException(
                status_code=404,
                detail="Invoice not found"
            )

        return payment

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )


# =========================================================
# GET PAYMENT BY ID
# =========================================================

@router.get(
    "/payments/{payment_id}",
    response_model=PaymentResponse
)
def get_payment_api(
    payment_id: int,
    db: Session = Depends(get_db)
):
    payment = get_payment(
        db=db,
        payment_id=payment_id
    )

    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return payment


# =========================================================
# GET PAYMENTS FOR INVOICE
# =========================================================

@router.get(
    "/invoices/{invoice_id}/payments",
    response_model=list[PaymentResponse]
)
def get_invoice_payments_api(
    invoice_id: int,
    db: Session = Depends(get_db)
):
    invoice_payments = get_invoice_payments(
        db=db,
        invoice_id=invoice_id
    )

    return invoice_payments


# =========================================================
# BILLING HEALTH / TEST
# =========================================================

@router.get("/")
def get_billing():
    return {
        "message": "Billing module is working"
    }