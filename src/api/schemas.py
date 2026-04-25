from pydantic import BaseModel
from typing import List, Optional


class SummaryResponse(BaseModel):
    product_id: str
    status: str
    summary: Optional[str]
    pros: List[str]
    cons: List[str]
    sentiment_overview: Optional[str]
    comment_count: int
    is_cached: bool
    message: Optional[str] = None
    last_generated_at: Optional[str] = None
    comments_hash: Optional[str] = None


class SummaryStatusResponse(BaseModel):
    product_id: str
    status: str
    has_summary: bool
    comment_count: int
    is_cached: bool
    last_generated_at: Optional[str] = None
    message: Optional[str] = None