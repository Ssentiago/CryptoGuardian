from starlette.requests import Request

from backend.core.log_config import get_logger

logger = get_logger(__name__)


async def log_request(request: Request, call_next):
    logger.info(f"Received request:")
    logger.info(f"Method: {request.method}")
    logger.info(f"URL: {request.url}")
    logger.info(f"Client host: {request.client.host}")
    logger.info(f"Headers: {request.headers}")
    logger.info(f"Query parameters: {request.query_params}")
    logger.info(f"Path parameters: {request.path_params}")
    logger.info(f"Query string: {request.query_params}")
    logger.info(f"Body: {await request.body()}")

    response = await call_next(request)

    logger.info(f"Responded with status code: {response.status_code}")

    return response
