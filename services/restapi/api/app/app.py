from fastapi import Depends, FastAPI, status

from api.app.routers.game import router as game_router
from api.app.verification import security

app: FastAPI = FastAPI(
    title="GuestReady Challenge REST API",
    docs_url="/",
    openapi_url="/openapi_url.json",
    dependencies=[Depends(security)],
)

# add the router with the guestready challenge endpoints
app.include_router(game_router)


@app.get("/version", tags=["Info"])
async def version() -> dict[str, str]:
    """
    Endpoint to get the version of the API.

    Returns:
        dict: A dictionary containing the version of the API.
    """
    return {"version": "1.0.0"}


# NOTE:  This is definitelty not the way to go, however I simply want an endpoint that where I can check if the API is up
@app.get("/health", tags=["HealthCheck"], status_code=status.HTTP_200_OK)
async def health() -> str:
    """
    Endpoint to check the health status of the API.

    Returns:
        str: A simple string "OK" indicating that the API is up and running.
    """
    return "OK"
