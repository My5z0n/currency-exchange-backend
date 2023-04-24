from api.core.exceptions import InternalServiceError, NoDataError, UserInputError
from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def get_exception_handlers():
    exception_handlers = {
        RequestValidationError: validation_exception_handler,
        UserInputError: validation_exception_handler,
        InternalServiceError: internal_service_exception_handler,
        NoDataError: no_data_exception_handler,
    }
    return exception_handlers


async def validation_exception_handler(request, exc):
    error_msg = {"message": "Unprocessable Request"}
    return JSONResponse(content=error_msg, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


async def internal_service_exception_handler(request, exc):
    error_msg = {"message": "Internal Service Error"}
    return JSONResponse(content=error_msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


async def no_data_exception_handler(request, exc):
    error_msg = {"message": "Data not found"}
    return JSONResponse(content=error_msg, status_code=status.HTTP_404_NOT_FOUND)
