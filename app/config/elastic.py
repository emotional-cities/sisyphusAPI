from elasticsearch import Elasticsearch
from app.config.logging import create_logger

logger = create_logger(name="app.config.client")

def get_db():
    # Create the client instance
    client = Elasticsearch(
        "http://elastic:9200"
    )

    logger.debug(client.info())

    return client