from elasticsearch import Elasticsearch
from app.config.logging import create_logger
from app.config.config import configuration as cfg

logger = create_logger(name="app.config.client")

def get_db():
    # Create the client instance
    client = Elasticsearch(
        f"http://{cfg.ELASTIC_HOST}:{cfg.ELASTIC_PORT}",
        opaque_id="sisyphusAPI"
    )

    logger.debug(client.info())

    return client