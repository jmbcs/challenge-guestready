import logging

from api.app.models import Developer, Game, Platform, Publisher
from api.app.responses import create_game_responses
from api.app.schemas import GameCreateResponse, GameSchema
from api.database.db import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router: APIRouter = APIRouter(tags=["GuestReady Challenge"], prefix="/guestready")
logger: logging.Logger = logging.getLogger(__name__)


@router.post(
    "/game",
    status_code=status.HTTP_201_CREATED,
    response_model=GameCreateResponse,
    responses=create_game_responses,
)
async def create_game(
    game: GameSchema, db: Session = Depends(get_db)
) -> GameCreateResponse:
    try:
        # VALIDATION - Check if the game already exists
        existing_game: Game | None = (
            db.query(Game)
            .filter(
                Game.title == game.title,
            )
            .first()
        )
        if existing_game:
            logger.debug(f"Game already exists: {existing_game}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "message": "A game with the same title already exists.",
                },
            )

        # Check if platform already exists, if not create it.
        platform: Platform | None = (
            db.query(Platform).filter(Platform.name == game.platform).first()
        )
        if not platform:
            platform = Platform(name=game.platform)
            db.add(platform)
            db.flush()
            logger.debug(f"Created new platform: {platform}")
        else:
            logger.debug(f"Found existing platform: {platform}")

        # Check if publisher already exists, if not create it.
        publisher: Publisher | None = (
            db.query(Publisher).filter(Publisher.name == game.publisher).first()
        )
        if not publisher:
            publisher = Publisher(name=game.publisher)
            db.add(publisher)
            db.flush()
            logger.debug(f"Created new publisher: {publisher}")
        else:
            logger.debug(f"Found existing publisher: {publisher}")

        # Check if developer already exists, if not create it.
        developer: Developer | None = (
            db.query(Developer).filter(Developer.name == game.developer).first()
        )
        if not developer:
            developer = Developer(name=game.developer)
            db.add(developer)
            db.flush()
            logger.debug(f"Created new developer: {developer}")
        else:
            logger.debug(f"Found existing developer: {developer}")

        # Create game
        new_game: Game = Game(
            title=game.title,
            genre=game.genre,
            platform=platform,
            publisher=publisher,
            developer=developer,
            release_date=game.release_date,
        )

        db.add(new_game)
        db.commit()
        db.refresh(new_game)
        logger.debug(f"Created new game: {new_game}")

        return GameCreateResponse(
            game=game,
        )

    except HTTPException as http_exc:
        db.rollback()
        logger.error(f"HTTP error occurred: {http_exc.detail}")
        raise http_exc

    except Exception as e:
        db.rollback()
        logger.error(f"An error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
