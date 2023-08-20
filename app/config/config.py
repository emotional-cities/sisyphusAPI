from typing import Optional

from loguru import logger
from pydantic import BaseSettings, Field


logger = logger.bind(name="app.core.config")


class GlobalConfig(BaseSettings):
    """Global configurations."""

    # This variable will be loaded from the .env file.
    # However, if there is a shell environment variable
    # having the same name, that will take precedence.

    ENV_STATE: Optional[str] = Field("dev", env="ENV_STATE")
    LOG_PATH: Optional[str] = Field("./logs", env="LOG_PATH")
    LOG_FILENAME: Optional[str] = Field("sisyphus.log", env="LOG_FILENAME")
    LOG_LEVEL: Optional[str] = Field("DEBUG", env="LOG_ROTATION")
    LOG_ROTATION: Optional[str] = Field("500 MB", env="LOG_ROTATION")
    LOG_RETENTION: Optional[str] = Field("10 days", env="LOG_RETENTION")
    LOG_FORMAT: Optional[str] = Field("{time} {level} {message}", env="LOG_FORMAT")

    class Config:
        """Loads the dotenv file."""

        env_file: str = ".env"


class DevConfig(GlobalConfig):
    """Development configurations."""

    ROOT_PATH: Optional[str] = Field(None, env="DEV_ROOT_PATH")
    LOG_LEVEL: Optional[str] = Field(None, env="DEV_LOG_LEVEL")
    SISYPHUS_DB_SERVER_HOST: Optional[str] = Field(
        None, env="DEV_SISYPHUS_DB_SERVER_HOST"
    )
    SISYPHUS_DB_SERVER_PORT: Optional[str] = Field(
        None, env="DEV_SISYPHUS_DB_SERVER_PORT"
    )
    SISYPHUS_DB_NAME: Optional[str] = Field(
        None, env="DEV_SISYPHUS_DB_NAME"
    )
    SISYPHUS_DB_USER: Optional[str] = Field(
        None, env="DEV_SISYPHUS_DB_USER"
    )
    SISYPHUS_DB_PASSWORD: Optional[str] = Field(
        None, env="DEV_SISYPHUS_DB_PASSWORD"
    )



class ProdConfig(GlobalConfig):
    """Production configurations."""

    ROOT_PATH: Optional[str] = Field(None, env="PROD_ROOT_PATH")
    LOG_LEVEL: Optional[str] = Field(None, env="PROD_LOG_LEVEL")
    SISYPHUS_DB_SERVER_HOST: Optional[str] = Field(
        None, env="PROD_SISYPHUS_DB_SERVER_HOST"
    )
    SISYPHUS_DB_SERVER_PORT: Optional[str] = Field(
        None, env="PROD_SISYPHUS_DB_SERVER_PORT"
    )
    SISYPHUS_DB_NAME: Optional[str] = Field(
        None, env="PROD_SISYPHUS_DB_NAME"
    )
    SISYPHUS_DB_USER: Optional[str] = Field(
        None, env="PROD_SISYPHUS_DB_USER"
    )
    SISYPHUS_DB_PASSWORD: Optional[str] = Field(
        None, env="PROD_SISYPHUS_DB_PASSWORD"
    )


class FactoryConfig:
    """Returns a config instance dependending on the ENV_STATE variable."""

    def __init__(self, env_state: Optional[str]):
        self.env_state = env_state

    def __call__(self):
        if self.env_state == "dev":
            return DevConfig()

        elif self.env_state == "prod":
            return ProdConfig()


configuration = FactoryConfig(GlobalConfig().ENV_STATE)()
logger.debug(f"Global config: {configuration.__repr__()}")
