import json
from fastapi import APIRouter, Depends, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from app.config.logging import create_logger
from app.config.elastic import get_db
from app.utils.csv_utils import csv_to_oarec
from elasticsearch import NotFoundError
from app.config.config import configuration as cfg


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
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={})

    try:
        # Clean index

        # Load new records
        for row in results:
            record_id = row["id"]
            elastic.index(index=cfg.ELASTIC_INDEX, id=record_id, body=json.dumps(row))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"message": repr(e)})


    return JSONResponse(status_code=status.HTTP_201_CREATED, content="Records inserted ")


@router.delete("/{record_id}", status_code=status.HTTP_200_OK)
async def deleteProtectedRecord(
    record_id: str,
    record_type: str,
    record_owner: str,
    elastic: get_db = Depends()):
        try:
            resp = elastic.get(index=cfg.ELASTIC_INDEX, id=record_id)
            print(record_owner)
            if resp['_source']['type'] == record_type and record_owner > '':
                pass
            else:
                return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"message": "You are not allowed to change this record"})
        except NotFoundError:
            # You cannot PUT on a not existing id
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "The ID does not exists"})

        # SAVE
        elastic.delete(index=cfg.ELASTIC_INDEX, id=record_id)