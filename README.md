<!-- TOC --><a name="challenge-guestready-django-developer"></a>

# Challenge - Guestready - Django Developer

- Read the [CHALLENGE.md](CHALLENGE.md)

## Table of Contents

<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Proposed Solution Architecture](#proposed-solution-architecture)
  - [Key Features:](#key-features)
- [Development Environment Setup](#development-environment-setup)
  - [Development and Debugging](#development-and-debugging)
  - [Additional Resources](#additional-resources)
- [Testing](#testing)
- [Video - Test](#video-test)

<!-- TOC end -->

<!-- toc -->

<!-- TOC --><a name="requirements"></a>

## Requirements

- Docker Compose: `v2.28.1`
- Make: `v4.3`

<!-- TOC --><a name="quick-start"></a>

## Quick Start and Deployment

1. Clone this repo.

   ```bash
   git clone https://github.com/jmbcs/challenge-guestready.git
   ```

2. Run `make run`

   - If `make` is **not installed**, you can use the following command instead:

     ```bash
     docker compose -f docker-compose.yml up --build -d --wait
     ```

   - Wait for services to become `healthy` (this should take less than 30s after building the images).

3. Access Django at [http://localhost:8000](http://localhost:8000)
4. Access FastAPI at [http://localhost:8001](http://localhost:8001)
   - User: `guestready`
   - Password: `test123`
   - Documentation for endpoints can be found at [http://localhost:8001/redoc](http://localhost:8001/redoc)

Watch the video below as a reference for the `Django` + `FastAPI` interaction.

<hr>
<details>
  <summary>
    <strong>CLICK HERE</strong> to show video of Django + FastAPI.
  </summary>
  <p align="center">
    <video src="https://github.com/jmbcs/challenge-guestready/assets/112523386/b7d6f3be-5ca6-4098-9e7b-bf01fd171bd1" controls width="640" height="360"></video>
  </p>
</details>
<hr>

<!-- TOC --><a name="proposed-solution-architecture"></a>

## Proposed Solution Architecture

<p align="center">
  <img src="images/architecture.png" width=400 />
</p>

<!-- TOC --><a name="key-features"></a>

### Key Features:

- Each service runs in its own Docker container.
- Each service provides logs.
- Each service waits for their dependecy to become healthy.
  - **Example**: `FastAPI` service will only connect to `PostgreSQL` after the container reports to be `healhy`.
- Service configurations are managed via environment variables using `pydantic` basesettings.
- Services communicate within the Docker network but are also exposed on the host for easy access.
- Database migrations for PostgreSQL are handled by `alembic` integrated with `FastAPI`.
- PostgreSQL database initialization includes setting up users and databases for the REST API service.

## Available commands

Run `make` to check the available commands

<p align="center">
  <img src="images/make_commands.png" width=600 />
</p>

<!-- TOC --><a name="development-environment-setup"></a>

## Setting Up Your Development Environment

1. **Install `direnv`**: Visit [direnv.net](https://direnv.net/) and follow the installation instructions for your operating system.

2. **Initialize `direnv`**: After installing `direnv`, run the command `direnv allow` in your project directory. This allows `direnv` to load the environment variables and any script specified in `.envrc` into your shell session automatically.

3. **Automatic Dependency Installation**: Ensure all dependencies are installed automatically once `direnv` is set up.

### Development and Debugging

- You can run either Django or FastAPI APIs directly from the terminal:
  - **Run Django**: Execute `make dev.django` in your terminal.
  - **Run FastAPI**: Execute `make dev.restapi` in your terminal.

For detailed guidance on using `direnv` and setting up your environment using the `.envrc` file, refer to the following video:

<hr>
<details>
  <summary>
    <strong>CLICK HERE</strong> to show video of direnv.
  </summary>
  <p align="center">
    <video src="https://github.com/jmbcs/challenge-guestready/assets/112523386/7cda6642-c9f9-46e2-bd42-a1e4ff663cea" controls width="640" height="360"></video>
  </p>
</details>
<hr>

<!-- TOC --><a name="video-test"></a>

## Testing - Code quality

To ensure comprehensive code quality, the `make tox` command performs the following tasks:

1. Executes all `pytest` tests for `fastapi`, located at [services/restapi/tests](services/restapi/tests).
2. Executes tests for `django`, specifically targeting tests located at [services/django/django_project/game/tests.py](services/django/django_project/game/tests.py).
3. Runs Pre-commit hooks across the repository to automatically enhance code formatting and perform other necessary checks.
4. Validates proper Python code using `mypy`.

You can check the output of the command `make tox` by refering to the video below.

<hr>
<details>
  <summary>
    <strong>CLICK HERE</strong> to show video of make tox.
  </summary>
  <img src="images/make_commands.png" width=600 />
  </p>
</details>
<hr>

## Testing - FastAPI Response Performance

- If you have `Postman`, `Thunder Client` or `Flashpost`, you can import the provided collection file to run all tests:

  - [.postman/guestready_challenge.postman_collection.json](.postman/guestready_challenge.postman_collection.json)

- This will have some requests already setup that you can use to test the endpoints.
<p align="center">
  <img src="images/collection.png" width=600 />
</p>

- Example for a `GET` request

<p align="center">
  <img src="images/collection_endpoint.png" width=600 />
</p>

<hr>
<details>
  <summary>
    <strong>CLICK HERE</strong> to show the peformance of the endpoint when receiving requests up to 100 Virtual Users (postman performance test).
  </summary>
  <p align="center">
    <img src="images/test_get_all_games.png" width=600 alt="Image showing results of retrieving all games.">
    <br>
    This image displays the results of a test for retrieving all games.
        <br>
    <strong>GET</strong>: http://localhost:8001/games
    <br>
    <br>
    <img src="images/test_get_games_by_dev.png" width=600 alt="Image showing results of retrieving games by developer.">
    <br>
      This image illustrates the test results for retrieving games filtered by developer.
    <br>
    <strong>GET</strong>: http://localhost:8001/games/{developer}
    <br>
    <br>
    <img src="images/test_get_games_filtered.png" width=600 alt="Image showing results of retrieving filtered games.">
    <br>
    In this image, the test results show games filtered based on certain criteria (with query params)
    <br>
    <strong>GET</strong>: http://localhost:8001/games
    <br>
    <br>
    <img src="images/test_post_game.png" width=600 alt="Image showing results of posting a new game.">
    <br>
    This image represents the test outcome of adding or posting a new game.
    <br>
    <strong>POST</strong>: http://localhost:8001/game
    <br>
  </p>
</details>
<hr>

## Logging

## PostgreSQL queries optimization

## Final Remarks and Suggestions
