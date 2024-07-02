from api.database.db import Base
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Platform(Base):
    """
    Represents a database model for storing information about platforms.
    """

    __tablename__ = "platform"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    games = relationship("Game", back_populates="platform")

    def __repr__(self):
        return f"<Platform(id={self.id}, name='{self.name}')>"


class Publisher(Base):
    """
    Represents a database model for storing information about publishers.
    """

    __tablename__ = "publisher"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    games = relationship("Game", back_populates="publisher")

    def __repr__(self):
        return f"<Publisher(id={self.id}, name='{self.name}')>"


class Developer(Base):
    """
    Represents a database model for storing information about developers.
    """

    __tablename__ = "developer"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    games = relationship("Game", back_populates="developer")

    def __repr__(self):
        return f"<Publisher(id={self.id}, name='{self.name}')>"


class Game(Base):
    """
    Represents a database model for storing information about video games.
    """

    __tablename__ = "game"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    platform_id = Column(Integer, ForeignKey("platform.id"), nullable=False)
    publisher_id = Column(Integer, ForeignKey("publisher.id"), nullable=False)
    developer_id = Column(Integer, ForeignKey("developer.id"), nullable=False)
    release_date = Column(Date, nullable=False)

    platform = relationship("Platform", back_populates="games")
    publisher = relationship("Publisher", back_populates="games")
    developer = relationship("Developer", back_populates="games")

    def __repr__(self):
        return (
            f"<Game(id={self.id}, title='{self.title}', genre='{self.genre}', "
            f"platform='{self.platform.name}', publisher='{self.publisher.name}', "
            f"release_date={self.release_date})>"
        )
