from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from datetime import date
from enum import Enum
from app.config.logging import create_logger
from app.config.elastic import get_db
from app.utils.csv_utils import csv_to_oarec

logger = create_logger(name="app.config.client")

router = APIRouter(
    prefix="/csv",
    tags=["csv"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_class=JSONResponse, status_code=status.HTTP_201_CREATED)
async def importMetadata(
    file: UploadFile = None,
    elastic: get_db = Depends()):

    results = []
    if file and file.content_type == "text/csv":
        content_as_bytes = await file.read()
        content_as_string = content_as_bytes.decode('utf-8')
        lines = content_as_string.splitlines()
        results = csv_to_oarec(lines)
    else:
        raise HTTPException(status_code=400, detail="Invalid file type")

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=results)