from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi.responses import JSONResponse
from datetime import date
from enum import Enum
from app.config.logging import create_logger
from app.config.elastic import get_db


logger = create_logger(name="app.config.client")

router = APIRouter(
    prefix="/csv",
    tags=["csv"],
    responses={404: {"description": "Not found"}},
)

@router.get("/status/")
async def healthcheck():
    return {"status": "healthy"}

@router.get("/export", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def exportMetadata(
    record_id: str,
    elastic: get_db = Depends()):
        pass