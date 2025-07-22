from fastapi import APIRouter

router = APIRouter(tags=['Authentication'])

@router.get("/")
def default():
    return "Hi, this is my first app"