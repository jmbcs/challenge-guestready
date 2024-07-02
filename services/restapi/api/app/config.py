from pydantic import BaseModel


class APIAuthentication(BaseModel):
    """
    Represents the authentication credentials required for API access.

    Attributes:
        user (str): The username for authentication.
        password (str): The password associated with the username.
    """

    user: str
    password: str


class APIConfig(BaseModel):
    """
    Represents the configuration settings for the API.

    Attributes:
        auth (APIAuthentication): The authentication credentials required for the API.
        port (int): The port number on which the API server is running.
    """

    auth: APIAuthentication
    port: int
