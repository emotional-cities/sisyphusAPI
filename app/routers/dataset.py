import json
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.config.logging import create_logger
from app.config.config import configuration as cfg


logger = create_logger(name="app.config.client")

router = APIRouter(
    prefix="/dataset",
    tags=["data"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_class=JSONResponse, status_code=status.HTTP_200_OK)
async def downloadDataset(record_id: str):

    return JSONResponse(status_code=status.HTTP_200_OK, content="")
