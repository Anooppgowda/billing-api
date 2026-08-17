class BillingException(Exception):
    """Base exception for billing-related errors."""
    pass


class CustomerNotFoundException(BillingException):
    """Raised when a customer does not exist."""
    pass


class InvoiceNotFoundException(BillingException):
    """Raised when an invoice does not exist."""
    pass


class PaymentNotFoundException(BillingException):
    """Raised when a payment does not exist."""
    pass


class InvalidPaymentException(BillingException):
    """Raised when a payment operation is invalid."""
    pass