import logging

import requests
from django.db import models
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django_project.settings import config
from requests.auth import HTTPBasicAuth
from rest_framework import status

from .models import Developer, Game, Platform, Publisher

logger: logging.Logger = logging.getLogger(__name__)


# Create your views here.
def front_page(request: HttpRequest) -> HttpResponse:
    """
    View function for rendering the front page of the application.

    This function renders the 'index.html' template which serves as the
    front page of the game application. It takes an HttpRequest object
    as an argument and returns an HttpResponse object with the rendered
    HTML content.
    """
    return render(request, 'game/front_page.html')


def get_games_from_api(request: HttpRequest) -> HttpResponse:
    """
    Fetches games data from an API endpoint and saves it into the database.

    Args:
        request: Django request object.

    Returns:
        Renders a success or error page based on the API response.

    Raises:
       JsonResponse: JSON response indicating success or error.

    """
    if not request.method == 'GET':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

    success_count: int = 0
    fail_count: int = 0

    try:
        response: requests.Response = requests.get(config.games_url)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        data = response.json()

        if not isinstance(data, list):
            raise TypeError('Response data is not of type list')

        # Loop through each game and try to create it in the django database

        for game_data in data:
            try:
                platform, _ = Platform.objects.get_or_create(name=game_data['platform'])
                publisher, _ = Publisher.objects.get_or_create(
                    name=game_data['publisher']
                )
                developer, _ = Developer.objects.get_or_create(
                    name=game_data['developer']
                )

                game, created = Game.objects.get_or_create(
                    title=game_data['title'],
                    genre=game_data['genre'],
                    description=game_data['short_description'],
                    release_date=game_data['release_date'],
                    platform=platform,
                    publisher=publisher,
                    developer=developer,
                )

                if created:
                    success_count += 1
                    logger.debug(f'Successfully imported {game.title}')
                else:
                    fail_count += 1
                    logger.warning(f'{game.title} already exists in the database')

            except Exception as e:
                fail_count += 1
                logger.error(f"Failed to import game {game_data['title']}: {str(e)}")

        context: dict[str, int | models.BaseManager[Game]] = {
            'success_count': success_count,
            'fail_count': fail_count,
            'total_games': len(data),
            'games': Game.objects.all(),
        }
        return render(
            request=request,
            template_name='game/success.html',
            context=context,
        )

    except Exception as e:
        logger.error(f'An unexpected error occurred: {str(e)}')
        return render(request=request, template_name='game/error.html')


def post_games(request: HttpRequest) -> HttpResponse:
    """
    Handles sending all game data to a FastAPI endpoint.

    Args:
        request: Django HTTP request object.

    Returns:
        JsonResponse: JSON response indicating success or error.
    """

    if not request.method == 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

    games: models.BaseManager[Game] = Game.objects.all()
    success_count: int = 0
    fail_count: int = 0

    # Loop through each game and send its data to the FastAPI endpoint
    for game in games:
        post_data = {
            'title': game.title,
            'genre': game.genre,
            'release_date': game.release_date.isoformat(),
            'description': game.description,
            'platform': game.platform.name,
            'publisher': game.publisher.name,
            'developer': game.developer.name,
        }

        response: requests.Response = requests.post(
            url=f'{config.fastapi.url}/game',
            json=post_data,
            auth=HTTPBasicAuth(config.fastapi.auth.user, config.fastapi.auth.password),
        )

        if response.status_code == status.HTTP_201_CREATED:
            success_count += 1
            logger.debug(response.text)
        else:
            fail_count += 1
            logger.warning(response.text)

    if fail_count == 0:
        logger.info(f'All {success_count} games sent successfully')
    else:
        logger.info(
            f'{success_count} games sent successfully, {fail_count} games failed',
        )

    context: dict[str, int] = {
        'fail_count': fail_count,
        'success_count': success_count,
        'total_games': len(games),
    }
    return render(request=request, template_name='game/post.html', context=context)
