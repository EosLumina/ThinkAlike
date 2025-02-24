from fastapi import APIRouter

router = APIRouter()

@router.get("/feedback")
async def read_feedback():
    return {"feedback": "This is the feedback route"}
