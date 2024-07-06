<!-- TOC --><a name="challenge-guestready-django-developer"></a>

# Challenge - Guestready - Django Developer

- Read the [CHALLENGE.md](CHALLENGE.md)

## Table of Contents

<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

- [Challenge - Guestready - Django Developer](#challenge-guestready-django-developer)
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

- Docker Compose : `v2.28.1`
- Make : `v4.3`

<!-- TOC --><a name="quick-start"></a>

## Quick Start

1. Run `make run`
   - Wait for services to be `healthy`(should take less than `30s` after building the images)
2. Access Django at [http://localhost:8000](http://localhost:8000)
3. Access FastAPI at [http://localhost:8001](http://localhost:8001)
   - User: `guestready`
   - Password: `test123`

Watch the video below as a reference for the `Django` service + `FastAPI`

https://github.com/jmbcs/challenge-guestready/assets/112523386/b7d6f3be-5ca6-4098-9e7b-bf01fd171bd1

<!-- TOC --><a name="proposed-solution-architecture"></a>

## Proposed Solution Architecture

![architecture](images/architecture.png)

<!-- TOC --><a name="key-features"></a>

### Key Features:

- Each service runs in its own Docker container.
- Service configurations are managed via environment variables using `pydantic` basesettings.
- Services communicate within the Docker network but are also exposed on the host for easy access.
- Database migrations for PostgreSQL are handled by `alembic` integrated with `FastAPI`.
- PostgreSQL database initialization includes setting up users and databases for the REST API service.

<!-- TOC --><a name="development-environment-setup"></a>

## Development Environment Setup

To set up your development environment, follow these steps:

1. Install `direnv` from [https://direnv.net/](https://direnv.net/).
2. Run `direnv allow` after installation.
3. This will install all dependencies automatically.

<!-- TOC --><a name="development-and-debugging"></a>

### Development and Debugging

- You can run either Django or the FastAPI API directly from the terminal for development/debugging purposes.

<!-- TOC --><a name="additional-resources"></a>

### Additional Resources

<!-- TOC --><a name="testing"></a>

## Testing

Reference the following video for guidance on using `direnv` to automatically set up your environment using the `.envrc` file

https://github.com/jmbcs/challenge-guestready/assets/112523386/7cda6642-c9f9-46e2-bd42-a1e4ff663cea

<!-- TOC --><a name="video-test"></a>

## Video - Test

https://github.com/jmbcs/challenge-guestready/assets/112523386/f4fe80d8-5a8e-4e3c-90af-3d257555db8a
