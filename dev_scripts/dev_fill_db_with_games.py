"""
This is a development script designed to populate the database with initial game data for development/testing purposes.
It reads game data from a JSON file and sends POST requests to a FastAPI endpoint to add each game to the database.
The script uses basic authentication for the API requests.


How it works:
1. Reads the game data from the specified JSON file.
2. Filters and structures the data to match the API requirements.
3. Sends POST requests to the FastAPI endpoint to add each game to the database.
4. Handles any request errors and prints relevant information.

Usage:
- Ensure the FastAPI server is running and accessible at the specified URL.
- Update the URL, AUTH_USER, AUTH_PASSWORD, and FILE_PATH variables as needed.
"""

import json
from typing import Any, Dict

import requests
from requests import Response

# FastAPI endpoint
URL: str = 'http://localhost:8000/game'

# Credentials for API authentication
AUTH_USER: str = 'admin'
AUTH_PASSWORD: str = 'test123'

# Path to the JSON file containing game data
FILE_PATH: str = 'dev_scripts/dev_games.json'


def add_game(game: dict[str, Any]) -> None:
    """
    Add a game to the database by sending a POST request to the API endpoint.

    Args:
        game (Dict[str, Any]): A dictionary containing game details.
    """
    try:
        # Filter and structure the game data to match the API requirements
        filtered_game: dict[str, Any] = {
            'title': game['title'],
            'description': game['short_description'],
            'developer': game['developer'],
            'genre': game['genre'],
            'release_date': game['release_date'],
            'publisher': game['publisher'],
            'platform': game['platform'],
        }
        # Send the POST request to the API endpoint
        response: Response = requests.post(
            URL, json=filtered_game, auth=(AUTH_USER, AUTH_PASSWORD)
        )
        # Raise an exception for any HTTP errors
        response.raise_for_status()

        # Print the response from the server
        print(f'Game added: {response.json()}')

    except requests.exceptions.RequestException as e:
        # Print the error if the request fails
        print(f'Failed to add game: {e}')


def load_games(file_path: str) -> list[Dict[str, Any]]:
    """
    Load JSON data from a file.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        Dict[str, Any]: The JSON data loaded from the file.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# Load the game data from the file
games_data: list[dict[str, Any]] = load_games(FILE_PATH)

# Iterate over each game in the data and add it to the database
for game in games_data:
    add_game(game)
