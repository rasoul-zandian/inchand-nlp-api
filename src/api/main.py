from fastapi import FastAPI, HTTPException
from src.api.schemas import SummaryResponse, SummaryStatusResponse
from src.services.comment_service import get_comments_by_product_id
from src.services.summary_service import (
    get_or_create_summary,
    force_refresh_summary,
    get_summary_status,
)
@app.get("/")
def root():
    return {
        "message": "Welcome to Inchand NLP API 🚀",
        "docs": "/docs",
        "health": "/api/v1/health"
    }
app = FastAPI(
    title="Inchand NLP API",
    description="API for product comment analysis and summarization",
    version="1.0.0"
)


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "ok",
        "service": "product-summary-api",
        "version": "1.0.0"
    }


@app.get("/api/v1/summary/{product_id}", response_model=SummaryResponse)
def get_product_summary(product_id: str):
    try:
        product_comments = get_comments_by_product_id(product_id)
        summary_data = get_or_create_summary(product_id, product_comments)
        return SummaryResponse(**summary_data)

    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected internal error: {str(e)}"
        )


@app.get("/api/v1/summary/{product_id}/status", response_model=SummaryStatusResponse)
def get_product_summary_status(product_id: str):
    try:
        product_comments = get_comments_by_product_id(product_id)
        status_data = get_summary_status(product_id, product_comments)
        return SummaryStatusResponse(**status_data)

    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected internal error: {str(e)}"
        )


@app.post("/api/v1/refresh/{product_id}", response_model=SummaryResponse)
def refresh_product_summary(product_id: str):
    try:
        product_comments = get_comments_by_product_id(product_id)
        summary_data = force_refresh_summary(product_id, product_comments)
        return SummaryResponse(**summary_data)

    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected internal error: {str(e)}"
        )