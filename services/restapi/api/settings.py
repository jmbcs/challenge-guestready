from typing import Tuple, Type

from api.app.config import APIConfig
from api.database.config import PostgresqlDBConfig

# from database.models import PostgresDBConfig
from api.logger import LoggerConfig
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource

_Config__SERVICE_PREFIX = "guestready__"


class Settings(BaseSettings):
    """
    Configuration settings for the application.

    Attributes:
        db (MongoDBConfig): Database configuration settings.
        api (APIAuthentication): API authentication settings.
    """

    # db: PostgresDBConfig
    api: APIConfig
    db: PostgresqlDBConfig
    logger: LoggerConfig

    class Config:
        """
        Configuration for the Settings class.

        Attributes:
            env_file (str): The environment file to load settings from.
            env_nested_delimiter (str): The delimiter for nested environment variables.
            env_file_encoding (str): The encoding of the environment file.
            env_prefix (str): The prefix for environment variables.
        """

        env_file = "restapi.env"
        env_nested_delimiter = "__"
        env_file_encoding = "utf-8"
        env_prefix = _Config__SERVICE_PREFIX

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        """
        Customizes the priority order of settings sources.

        Args:
            settings_cls (Type[BaseSettings]): The settings class.
            init_settings (PydanticBaseSettingsSource): Initial settings source.
            env_settings (PydanticBaseSettingsSource): Environment settings source.
            dotenv_settings (PydanticBaseSettingsSource): Dotenv settings source.
            file_secret_settings (PydanticBaseSettingsSource): File secret settings source.

        Returns:
            Tuple[PydanticBaseSettingsSource, ...]: A tuple of settings sources in the desired order.
        """
        return (
            env_settings,
            dotenv_settings,
            init_settings,
            file_secret_settings,
        )


# Create an instance of the Settings class
config = Settings()  # type: ignore
