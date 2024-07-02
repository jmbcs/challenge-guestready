from api.database.db import Base
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Platform(Base):
    """
    Represents a platform entity in the database.

    Attributes:
        id (int): The primary key and unique identifier for each platform.
        name (str): The name of the platform, which must be unique and not null.
        games (list[Game]): The list of games available on this platform, defined through the relationship with the Game model.
    """

    __tablename__ = "platform"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    games = relationship("Game", back_populates="platform")

    def __repr__(self):
        return f"<Platform(id={self.id}, name='{self.name}')>"


class Publisher(Base):
    """
    Represents a publisher entity in the database.

    Attributes:
        id (int): The primary key and unique identifier for each publisher.
        name (str): The name of the publisher, which must be unique and not null.
        games (list[Game]): The list of games published by this publisher, defined through the relationship with the Game model.
    """

    __tablename__ = "publisher"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    games = relationship("Game", back_populates="publisher")

    def __repr__(self):
        return f"<Publisher(id={self.id}, name='{self.name}')>"


class Developer(Base):
    """
    Represents a developer entity in the database.

    Attributes:
        id (int): The primary key and unique identifier for each developer.
        name (str): The name of the developer, which must be unique and not null.
        games (list[Game]): The list of games developed by this developer, defined through the relationship with the Game model.
    """

    __tablename__ = "developer"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    games = relationship("Game", back_populates="developer")

    def __repr__(self):
        return f"<Developer(id={self.id}, name='{self.name}')>"


class Game(Base):
    """
    Represents a video game entity in the database.

    Attributes:
        id (int): The primary key and unique identifier for each game.
        title (str): The title of the game, which cannot be null.
        genre (str): The genre of the game, which cannot be null.
        release_date (date): The release date of the game, which cannot be null.
        platform_id (int): The foreign key linking to the platform the game is available on.
        publisher_id (int): The foreign key linking to the publisher of the game.
        developer_id (int): The foreign key linking to the developer of the game.
        platform (Platform): The platform on which the game is available, defined through the relationship with the Platform model.
        publisher (Publisher): The publisher of the game, defined through the relationship with the Publisher model.
        developer (Developer): The developer of the game, defined through the relationship with the Developer model.
    """

    __tablename__ = "game"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    release_date = Column(Date, nullable=False)

    platform_id = Column(Integer, ForeignKey("platform.id"), nullable=False)
    publisher_id = Column(Integer, ForeignKey("publisher.id"), nullable=False)
    developer_id = Column(Integer, ForeignKey("developer.id"), nullable=False)

    platform = relationship("Platform", back_populates="games")
    publisher = relationship("Publisher", back_populates="games")
    developer = relationship("Developer", back_populates="games")

    def __repr__(self):
        return f"<Game(id={self.id}, title='{self.title}', release_date={self.release_date}, genre='{self.genre}', platform='{self.platform.name}', publisher='{self.publisher.name}', developer='{self.developer.name}')>"
