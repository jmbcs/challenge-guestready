import logging

from api.app.models import Developer, Game, Platform, Publisher
from api.app.schemas import GameSchema
from api.database.db import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router: APIRouter = APIRouter(tags=["GuestReady Challenge"], prefix="/guestready")
logger: logging.Logger = logging.getLogger(__name__)


@router.post("/game", status_code=status.HTTP_201_CREATED)
async def create_game(request: GameSchema, db: Session = Depends(get_db)):
    try:
        with db.begin():
            # Check or create platform
            platform = (
                db.query(Platform).filter(Platform.name == request.platform).first()
            )
            if not platform:
                platform = Platform(name=request.platform)
                db.add(platform)
                db.flush()
            logger.debug(f"Platform: {platform}")

            # Check or create publisher
            publisher = (
                db.query(Publisher).filter(Publisher.name == request.publisher).first()
            )
            if not publisher:
                publisher = Publisher(name=request.publisher)
                db.add(publisher)
                db.flush()
            logger.debug(f"Publisher: {publisher}")

            # Check or create developer
            developer = (
                db.query(Developer).filter(Developer.name == request.developer).first()
            )
            if not developer:
                developer = Developer(name=request.developer)
                db.add(developer)
                db.flush()

            logger.debug(f"Developer: {developer}")

            # Create game
            game = Game(
                title=request.title,
                genre=request.genre,
                platform=platform,
                publisher=publisher,
                developer=developer,
                release_date=request.release_date,
            )
            db.add(game)
            db.commit()
            db.refresh(game)

        return {"message": "Game created successfully", "game": game}

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
