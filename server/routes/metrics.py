from fastapi import APIRouter
from controllers import metrics

router = APIRouter()

@router.get("/general")
def get_data():
    return metrics.get_data()