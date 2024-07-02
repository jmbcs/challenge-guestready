from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator


class PlatformSchema(BaseModel):
    """
    Schema representing the details of a platform.

    Attributes:
        name (str): The name of the platform.\n
    """

    name: str = Field(description="The name of the platform.")


class PublisherSchema(BaseModel):
    """
    Schema representing the details of a publisher.

    Attributes:
        name (str): The name of the publisher.\n
    """

    name: str = Field(description="The name of the publisher.")


class DeveloperSchema(BaseModel):
    """
    Schema representing the details of a developer.

    Attributes:
        name (str): The name of the developer.\n
    """

    name: str = Field(description="The name of the developer.")


class GameSchema(BaseModel):
    """
    Schema representing the details of a game.

    Attributes:
        title (str): The title of the game.\n
        genre (str): The genre of the game.\n
        release_date (date): The release date of the game.\n
        platform (str): The name of the platform on which the game is available.\n
        publisher (str): The name of the publisher of the game.\n
        developer (str): The name of the developer of the game.\n
    """

    title: str = Field(description="The title of the game.")
    genre: str = Field(description="The genre of the game.")
    release_date: date = Field(description="The release date of the game.")

    platform: str = Field(
        description="The name of the platform on which the game is available."
    )
    publisher: str = Field(description="The name of the publisher of the game.")
    developer: str = Field(description="The name of the developer of the game.")

    @field_validator("release_date")
    def validate_release_date(cls, v):
        """
        Validate the release date to ensure it is not in the future.

        Args:
            v (date): The release date to validate.\n

        Raises:
            ValueError: If the date is in the future.\n

        Returns:
            date: The validated release date.\n
        """
        if v > date.today():
            raise ValueError("Release date cannot be in the future.")
        return v


# Pydantic model for the response message
class GameCreateResponse(BaseModel):
    message: str = "Game created successfully."
    game: GameSchema
