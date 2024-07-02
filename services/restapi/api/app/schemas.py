from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class PlatformSchema(BaseModel):
    """
    Schema representing the details of a platform.

    Attributes:
        name (str): The name of the platform.
    """

    name: str = Field(description="The name of the platform.")


class PublisherSchema(BaseModel):
    """
    Schema representing the details of a publisher.

    Attributes:
        name (str): The name of the publisher.
    """

    name: str = Field(description="The name of the publisher.")


class DeveloperSchema(BaseModel):
    """
    Schema representing the details of a developer.

    Attributes:
        name (str): The name of the developer.
    """

    name: str = Field(description="The name of the developer.")


class GameSchema(BaseModel):
    """
    Schema representing the details of a game.

    Attributes:
        title (str): The title of the game.
        genre (str): The genre of the game.
        release_date (str): The release date of the game in the format YYYY-MM-DD.
        platform (str): The name of the platform on which the game is available.
        publisher (str): The name of the publisher of the game.
        developer (str): The name of the developer of the game.
    """

    title: str = Field(description="The title of the game.")
    genre: str = Field(description="The genre of the game.")
    release_date: str = Field(
        description="The release date of the game in the format YYYY-MM-DD."
    )

    platform: str = Field(
        None, description="The name of the platform on which the game is available."
    )
    publisher: str = Field(None, description="The name of the publisher of the game.")
    developer: str = Field(None, description="The name of the developer of the game.")

    @field_validator("release_date")
    def validate_release_date(cls, v):
        """
        Validate the release date to ensure it is in the correct format and not in the future.

        Args:
            v (str): The release date to validate.

        Raises:
            ValueError: If the date is not in the format YYYY-MM-DD or is in the future.

        Returns:
            str: The validated release date.
        """
        try:
            release_date = datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Release date must be in the format YYYY-MM-DD.")
        if release_date > datetime.now():
            raise ValueError("Release date cannot be in the future.")
        return v
