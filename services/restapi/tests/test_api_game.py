import base64
import os
from datetime import date

import pytest
from api.app.app import app
from api.app.models import Developer, Game, Platform, Publisher
from api.database.db import Base, get_db
from api.settings import config
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

TEST_DATABASE_URL: str = "sqlite:///./test.db"

# Create a new engine instance
engine: Engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Create a configured "Session" class
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# Override the dependency to use the testing database session
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Apply the dependency override
app.dependency_overrides[get_db] = override_get_db

# Create all the tables in the test database
Base.metadata.create_all(bind=engine)

client: TestClient = TestClient(app)


def _get_auth_headers() -> dict[str, str]:
    """
    Generate the authorization headers required for accessing protected endpoints.

    Returns:
        dict[str, str]: A dictionary containing the authorization headers.
    """
    credentials: str = f"{config.api.auth.user}:{config.api.auth.password}"
    encoded_credentials: str = base64.b64encode(credentials.encode("utf-8")).decode(
        "utf-8",
    )
    headers: dict[str, str] = {"Authorization": f"Basic {encoded_credentials}"}
    return headers


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_db():
    """
    Clean up the test database after all tests have run.
    """
    yield
    try:
        os.remove("./test.db")
    except FileNotFoundError:
        pass


@pytest.fixture(scope="session")
def db_session():
    """
    Provide a SQLAlchemy session for database interactions.
    """
    session = TestingSessionLocal()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(scope="session")
def create_test_data(db_session):
    """
    Create test data for the database.
    """
    platform: Platform = Platform(name="Test Platform")
    developer: Developer = Developer(name="Test Developer")
    publisher: Publisher = Publisher(name="Test Publisher")
    game1: Game = Game(
        title="Game 1",
        genre="Action",
        description="Description of Game 1",
        platform=platform,
        developer=developer,
        publisher=publisher,
        release_date=date(2024, 1, 1),
    )
    game2: Game = Game(
        title="Game 2",
        genre="Adventure",
        description="Description of Game 2",
        platform=platform,
        developer=developer,
        publisher=publisher,
        release_date=date(2023, 12, 31),
    )

    db_session.add(platform)
    db_session.add(developer)
    db_session.add(publisher)
    db_session.add(game1)
    db_session.add(game2)
    db_session.commit()

    yield  # Yield to let tests run


@pytest.mark.parametrize(
    "query_params, expected_status_code, expected_titles",
    [
        ({}, status.HTTP_200_OK, ["Game 1", "Game 2"]),  # No filters
        (
            {"genre": "Action"},
            status.HTTP_200_OK,
            ["Game 1"],
        ),  # Filter by genre
        (
            {"release_date": "2024-01-01"},
            status.HTTP_200_OK,
            ["Game 1"],
        ),  # Filter by release_date
        (
            {"platform": "Test Platform"},
            status.HTTP_200_OK,
            ["Game 1", "Game 2"],
        ),  # Filter by platform
        (
            {"genre": "Adventure", "release_date": "2023-12-31"},
            status.HTTP_200_OK,
            ["Game 2"],
        ),  # Multiple filters
        (
            {"platform": "Nonexistent Platform"},
            status.HTTP_200_OK,
            [],
        ),  # Nonexistent platform
    ],
)
def test_get_games(
    query_params,
    expected_status_code,
    expected_titles,
    create_test_data,
):
    """
    Test the /games endpoint with various query parameters.
    """
    response = client.get(
        "/games",
        params=query_params,
        headers=_get_auth_headers(),
    )
    assert response.status_code == expected_status_code
    if expected_status_code == status.HTTP_200_OK:
        returned_titles = [game["title"] for game in response.json()]
        assert all(title in returned_titles for title in expected_titles)


def test_get_games_by_developer(create_test_data):
    """
    Test the /games/{developer} endpoint with a valid developer.
    """
    response = client.get("/games/Test Developer", headers=_get_auth_headers())
    assert response.status_code == status.HTTP_200_OK
    returned_titles = [game["title"] for game in response.json()]
    assert "Game 1" in returned_titles
    assert "Game 2" in returned_titles


def test_get_games_by_nonexistent_developer(create_test_data):
    """
    Test the /games/{developer} endpoint with a non-existent developer.
    """
    response = client.get(
        "/games/Nonexistent Developer",
        headers=_get_auth_headers(),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Developer not found"


def test_create_game(create_test_data):
    """
    Test creating a new game.
    """
    game_data: dict[str, str] = {
        "title": "New Test Game",
        "genre": "Adventure",
        "description": "A new test game",
        "platform": "Test Platform",
        "developer": "Test Developer",
        "publisher": "Test Publisher",
        "release_date": "2023-12-31",
    }

    response = client.post(
        "/game",
        json=game_data,
        headers=_get_auth_headers(),
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["game"]["title"] == "New Test Game"


def test_create_existing_game(create_test_data):
    """
    Test creating a game with a title that already exists.
    """
    game_data: dict[str, str] = {
        "title": "Game 1",
        "genre": "Action",
        "description": "A duplicate test game",
        "platform": "Test Platform",
        "developer": "Test Developer",
        "publisher": "Test Publisher",
        "release_date": "2024-01-01",
    }

    response = client.post(
        "/game",
        json=game_data,
        headers=_get_auth_headers(),
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert (
        response.json()["detail"]["message"]
        == f'A game with the same title {game_data["title"]} already exists.'
    )


def test_create_game_missing_fields(create_test_data):
    """
    Test creating a game with missing required fields.
    """
    game_data: dict[str, str] = {
        "title": "Incomplete Game",
        "genre": "Action",
    }

    response = client.post(
        "/game",
        json=game_data,
        headers=_get_auth_headers(),
    )
    assert (
        response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    )  # Unprocessable Entity
    assert "detail" in response.json()
