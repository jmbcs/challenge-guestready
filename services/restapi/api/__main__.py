import asyncio
import logging

from api.app.app import app
from api.settings import config
from hypercorn.asyncio import serve
from hypercorn.config import Config

# Configure logging
config.logger.configure_logger()
logger = logging.getLogger(__name__)


# Configure Hypercorn server settings
hypercorn_cfg: Config = Config()
hypercorn_cfg.bind = [f'0.0.0.0:{config.api.port}']
hypercorn_cfg.loglevel = str(logging.getLevelName(logger.getEffectiveLevel()))
hypercorn_cfg.accesslog = logger


async def _launch_api():
    """
    Launches the Hypercorn server to serve the API.

    Raises:
        Exception: If any error occurs while running the server.
    """
    logger.info('Starting API server...')
    try:
        await serve(app, hypercorn_cfg)  # type:ignore
    except Exception as e:
        logger.error(f'Error while running the server: {e}')
    finally:
        logger.info('Server shutdown complete.')


def run():
    """
    Runs the asyncio event loop to start the API server.

    Handles KeyboardInterrupt to gracefully shutdown the server.
    """
    try:
        asyncio.run(_launch_api())
    except KeyboardInterrupt:
        logger.info('Received exit signal. Shutting down gracefully.')
    except Exception as e:
        logger.error(f'Unexpected error: {e}')
    finally:
        logger.info('Application stopped.')


if __name__ == '__main__':
    run()
