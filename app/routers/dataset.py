from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse, JSONResponse
from app.config.logging import create_logger
from app.config.config import configuration as cfg
from pathlib import Path


logger = create_logger(name="app.config.client")

router = APIRouter(
    prefix="/dataset",
    tags=["data"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{record_id}", status_code=status.HTTP_200_OK)
async def downloadDataset(record_id: str, f: str):

    filename= ''
    filepath= ''
    mediatype= ''
    if(f and f.upper() == 'GEOJSON'):
        filename = record_id + '.geojson'
        filepath = cfg.GEOJSON_PATH + '/' + filename
        mediatype= 'application/geo+json'
    elif(f and f.upper() == 'GEOPACKAGE'):
        filename = record_id + '.geopackage'
        filepath = cfg.GEOPACKAGE_PATH + '/' + filename
        mediatype= 'application/x-sqlite3'
    elif(f and f.upper() == 'GEOPARQUET'):
        filename = record_id + '.gpkg'
        filepath = cfg.GEOPARQUET_PATH + '/' + filename
        mediatype= 'application/vnd.apache.parquet'
    else:
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"message": "Format non supported"})
    
    path = Path(filepath)
    if path.is_file():

        def iterfile():
            with open(filepath, mode='rb') as f:
                yield from f

        headers = {'Content-Disposition': 'attachment; filename="' + filename + '"'}
        return StreamingResponse(iterfile(), headers=headers, media_type=mediatype)
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Requested document does not exist"})
