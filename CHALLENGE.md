# Project Overview

- Create `django` + `fastapi+sqlalchemy`service

## 1. Django Service

### Models

#### Game Model

- `title`
- `description`
- `genre`
- `release date`

#### Publisher Model

- `name`

#### Developer Model

- `name`

#### Platform Model

- `name`

#### Relationships

- `Publisher`, `Developer`, and `Platform` should be related to `Game`.

### Page with Buttons

- **1st Button**:

  - Retrieve games data from `https://www.freetogame.com/api/games`
  - Save the retrieved data in the database using created models.

- **2nd Button**:
  - Get all stored games with related data.
  - Send the data to the FastAPI service using REST API.

## 2. FastAPI + SQLAlchemy Service

### Endpoints

- **Receive Data**:

  - Receive data from the Django service.
  - Store the received data in the database.

- **Display All Games**:

  - Implement an endpoint to display all stored games data in JSON format.

- **Filter Games**:

  - Implement filtering for the previous endpoint by `genre`, `platform`, `release date`.

- **Games by Developer**:
  - Implement an endpoint to display all games for a specified (by user) `developer`.

## Final Notes

- Ensure to optimize database queries.
- There are no specific requirements for the UI part; it can be very simple.
- Use any SQL database, preferably PostgreSQL.
- Don't forget to write a README file in repositories with a guide on how to run the projects.
