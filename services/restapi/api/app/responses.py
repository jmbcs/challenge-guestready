from typing import Any

from fastapi import status

create_game_responses: dict[int | str, dict[str, Any]] = {
    status.HTTP_201_CREATED: {
        "description": "Created - Game added to the database successfully.",
        "content": {
            "application/json": {
                "example": {
                    "message": "Game created successfully.",
                    "game": {
                        "title": "Example Game",
                        "genre": "Action",
                        "release_date": "2023-06-01",
                        "platform": "PC",
                        "publisher": "Example Publisher",
                        "developer": "Example Developer",
                    },
                }
            }
        },
    },
    status.HTTP_409_CONFLICT: {
        "description": "Conflict - Game already exists.",
        "content": {
            "application/json": {
                "example": {
                    "detail": {
                        "message": "A game with the same title already exists.",
                    },
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Internal Server Error - Something went wrong.",
        "content": {
            "application/json": {
                "example": {
                    "detail": {
                        "message": "An unexpected error occurred while creating the game.",
                        "error": "Internal Server Error",
                    },
                }
            }
        },
    },
}


get_game_responses: dict[int | str, dict[str, Any]] = {
    status.HTTP_200_OK: {
        "description": "Found - Games returned from the database",
        "content": {
            "application/json": {
                "example": {
                    "message": "Game created successfully.",
                    "game": {
                        "title": "Example Game",
                        "genre": "Action",
                        "release_date": "2023-06-01",
                        "platform": "PC",
                        "publisher": "Example Publisher",
                        "developer": "Example Developer",
                    },
                }
            }
        },
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Not Found - No games have been found.",
        "content": {
            "application/json": {
                "example": {
                    "detail": {
                        "message": "No game found based on parameters",
                    },
                }
            }
        },
    },
}
