from pydantic import BaseModel
from typing import Optional

class PRReviewRequest(BaseModel):
    owner: str
    pull_number: int
    repo: str


class PRReviewResponse(BaseModel):
    success: bool
    message: str
    inline_review_description: Optional[str] = None
    inline_reviews_count: int

class ErrorResponse(BaseModel):
    detail: str
