import json
from typing import Optional
from fastapi import APIRouter, Depends, Body, HTTPException, status
from fastapi.responses import JSONResponse
from datetime import date
from enum import Enum
from app.config.logging import create_logger
from app.config.elastic import get_db
from elasticsearch import NotFoundError
from app.utils.app_exceptions import AppException
from app.utils.ogcarec_utils import validate
from app.config.config import configuration as cfg

logger = create_logger(name="app.config.client")

router = APIRouter(
    prefix="/metadata",
    tags=["metadata"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{record_id}", response_class=JSONResponse, status_code=status.HTTP_200_OK)
async def getMetadata(
    record_id: str,
    elastic: get_db = Depends()):
        try:
            resp = elastic.get(index=cfg.ELASTIC_INDEX, id=record_id)
        except NotFoundError:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=None)

        if 'm' in resp['_source'].keys():
            resp['_source'].pop("m")

        return JSONResponse(status_code=status.HTTP_200_OK, content=resp['_source'])

@router.post("/{record_id}", response_class=JSONResponse, status_code=status.HTTP_201_CREATED)
async def postMetadata(
    record_id: str,
    document: dict = Body(...),
    elastic: get_db = Depends()):

        try:
            elastic.get(index=cfg.ELASTIC_INDEX, id=record_id)
            # You cannot POST on an existing id
            return JSONResponse(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, content={"message": "Another record exists with this ID"})
        except NotFoundError:
            pass

        # VALIDATION
        valid= validate(record_id, document)
        if valid['status'] == False:
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"message": valid['reason']})

        # ADD API MARK
        document['m'] = 'API'

        # SAVE
        elastic.index(index=cfg.ELASTIC_INDEX, id=record_id, body=json.dumps(document))

@router.put("/{record_id}", status_code=status.HTTP_200_OK)
async def putMetadata(
    record_id: str,
    document: dict = Body(...),
    elastic: get_db = Depends()):
        try:
            resp = elastic.get(index=cfg.ELASTIC_INDEX, id=record_id)
            if 'm' in resp['_source'].keys() and resp['_source']['m'] == 'API':
                pass
            else:
                return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"message": "You are not allowed to change this record"})
        except NotFoundError:
            # You cannot PUT on a not existing id
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "The ID does not exists"})

        # VALIDATION
        valid= validate(record_id, document)
        if valid['status'] == False:
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"message": valid['reason']})

        # ADD API MARK
        document['m'] = 'API'

        # SAVE
        elastic.index(index=cfg.ELASTIC_INDEX, id=record_id, body=json.dumps(document))

@router.delete("/{record_id}", status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def deleteMetadata(
    record_id: str,
    elastic: get_db = Depends()):
        pass

#                   ====-_      _-====___
#            _--^^^#####//      \#####^^^--_
#         _-^##########// (    ) \\##########^-_
#        -############//  |\^^/|  \\############-
#      _/############//   (@::@)   \\############\_
#     /#############((     \\//     ))#############\
#    -###############\\    (oo)    //###############-
#   -#################\\  / "" \  //#################-
#  -###################\\/       //###################-
# _#/|##########/\######(  \\//  )######/\##########|\#_