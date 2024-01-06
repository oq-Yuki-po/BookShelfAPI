import traceback
from functools import wraps
from logging import getLogger

from fastapi import HTTPException

from app.exceptions.message import ExceptionMessage
from app.models import session

app_logger = getLogger('app')


def handle_errors(func):
    """
    handle_errors is a decorator that handles errors.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException as exc:
            app_logger.error(exc)
            app_logger.error(traceback.format_exc())
            raise exc
        except Exception as exc:
            app_logger.error(exc)
            app_logger.error(traceback.format_exc())
            raise HTTPException(detail=ExceptionMessage.INTERNAL_SERVER_ERROR, status_code=500) from exc
        finally:
            session.close()

    return wrapper
