from app.core.config import env_conf
from fastapi import HTTPException,status
from app.routes.github.utils import pr_review
class Actions:
  async def post_pr_review(self,payload):
    state = {
        "owner": payload.owner,
        "pull_number": payload.pull_number,
        "repo": payload.repo,
    }

    requested_user = state.get("owner")
    if requested_user != env_conf.OWNER_USERNAME:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorized")

    try:
       result = pr_review(state.get("owner"),pull_number=state.get("pull_number"),repo=state.get("repo"))
       # Update state with result data if pr_review returns state
       if result:
           state.update(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}")

    return {
        "success": True,
        "message": "Review processed",
        "inline_review_description": state.get("inline_review_description"),
        "inline_reviews_count": len(state.get("inline_reviews") or []),
    }

actions = Actions()