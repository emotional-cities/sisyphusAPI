import json
from fastapi import APIRouter, Depends, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from app.config.logging import create_logger
from app.config.elastic import get_db
from app.utils.csv_utils import csv_to_oarec
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

    print(results)

    try:
        for row in results:
            record_id = row["id"]
            elastic.index(index=cfg.ELASTIC_INDEX, id=record_id, body=json.dumps(row))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"message": repr(e)})


    # return JSONResponse(status_code=status.HTTP_201_CREATED, content="Record inserted ")
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=results)