import base64

from api.app.app import app
from api.settings import config
from fastapi.testclient import TestClient
from httpx import Response

client: TestClient = TestClient(app)


def _get_auth_headers() -> dict[str, str]:
    """
    Generate the authorization headers required for accessing protected endpoints.

    Returns:
        dict[str, str]: A dictionary containing the authorization headers.
    """
    # Create the credentials string in the format "user:password"
    credentials: str = f'{config.api.auth.user}:{config.api.auth.password}'

    # Encode the credentials in base64
    encoded_credentials: str = base64.b64encode(credentials.encode('utf-8')).decode(
        'utf-8'
    )

    # Create the headers dictionary with the Authorization header
    headers: dict[str, str] = {'Authorization': f'Basic {encoded_credentials}'}

    return headers


def test_health():
    """
    Test the /health endpoint to ensure it returns a status code of 200
    and the expected response JSON.
    """
    # Send a GET request to the /health endpoint with the authorization headers
    response: Response = client.get('/health', headers=_get_auth_headers())

    # Define the expected JSON response
    expected_response_json: str = 'OK'
    # Define the expected status_code response
    expected_response_status_code: int = 200

    # Assert that the response status code is 200 (OK)
    assert (
        response.status_code == expected_response_status_code
    ), f'Expected status code {expected_response_status_code}, but got {response.status_code}'

    # Assert that the response JSON matches the expected value
    assert (
        response.json() == expected_response_json
    ), f"Expected response JSON '{expected_response_json}', but got {response.json()}"


def test_version():
    """
    Test the /version endpoint to ensure it returns a status code of 200
    and the expected response JSON.
    """
    # Send a GET request to the /version endpoint with the authorization headers
    response: Response = client.get('/version', headers=_get_auth_headers())

    # Define the expected JSON response
    expected_response_json: dict[str, str] = {'version': '1.0.0'}
    # Define the expected status_code response
    expected_response_status_code: int = 200

    # Assert that the response status code is 200 (OK)
    assert (
        response.status_code == expected_response_status_code
    ), f'Expected status code {expected_response_status_code}, but got {response.status_code}'

    # Assert that the response JSON matches the expected value
    assert (
        response.json() == expected_response_json
    ), f'Expected response JSON {expected_response_json}, but got {response.json()}'
