from fastapi import FastAPI
from app.api.routes.billing import router as billing_router

app = FastAPI(
    title="Billing API",
    description="Billing API team collaboration project",
    version="1.0.0"
)

app.include_router(billing_router)


@app.get("/")
def root():
    return {
        "message": "Billing API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }