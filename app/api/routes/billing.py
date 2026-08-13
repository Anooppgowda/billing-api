from fastapi import APIRouter

router = APIRouter(
    prefix="/billing",
    tags=["Billing"]
)


@router.get("/")
def get_billing():
    return {
        "message": "Billing API endpoint is working"
    }