from fastapi import APIRouter, HTTPException, status
from app.routes.github.actions import actions
from app.routes.github.schema import PRReviewRequest,PRReviewResponse,ErrorResponse


router = APIRouter()

@router.post(
    "/review", 
    status_code=status.HTTP_200_OK,
    response_model=PRReviewResponse,
    responses={
        200: {"model": PRReviewResponse, "description": "Review processed successfully"},
        403: {"model": ErrorResponse, "description": "Not authorized"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def post_pr_review(payload: PRReviewRequest):
    return await actions.post_pr_review(payload)


