import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from settings import config

logger = logging.getLogger(__name__)

# Define the security scheme for HTTP Basic Authentication
security: HTTPBasic = HTTPBasic()

# Define a dictionary to store user information
users: dict[str, dict[str, str | bool]] = {
    config.api.auth.user: {
        "password": config.api.auth.password,
        "token": "",
        "priviliged": True,
    },
}


def verification(creds: HTTPBasicCredentials = Depends(security)) -> bool:
    """
    Verify the provided credentials against the stored user information.

    Args:
        creds (HTTPBasicCredentials): The credentials provided by the user.

    Returns:
        bool: True if the credentials are valid else raise HTTPException (401)

    Raises:
        HTTPException: If the credentials are incorrect, an HTTP 401 Unauthorized
        exception is raised with the detail "Incorrect email or password" and the
        header "WWW-Authenticate: Basic".
    """
    username: str = creds.username
    password: str = creds.password
    if username in users and password == users[username]["password"]:
        logger.debug("User Authenticated")
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
