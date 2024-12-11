from fastapi import APIRouter

from api.routes.user import models


router = APIRouter(
    prefix="/api/py/doc",
    tags=["doc"],
)

@router.get("/base_test/", response_model=models.BaseDBModel)
def base_test(base_model: models.BaseDBModel):
    return base_model