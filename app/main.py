from fastapi import FastAPI
from api.api_v1.router import router as api_router_v1
from api.core.config import Settings
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from api.core.exceptions import UserInputError
from app.api.core.exceptions import InternalServiceError


def get_application() -> FastAPI:
    application = FastAPI(title="Python Backend NBP",
                          debug=Settings.DEBUG_MODE)
    application.include_router(api_router_v1, prefix="/api/v1")
    return application


app = get_application()


@app.exception_handler(RequestValidationError)
@app.exception_handler(UserInputError)
async def validation_exception_handler(request, exc):
    error_msg = {"message": "Invalid Request"}
    return JSONResponse(content=error_msg, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.exception_handler(InternalServiceError)
async def internal_service_exception_handler(request, exc):
    error_msg = {"message": "Internal Service Error"}
    return JSONResponse(content=error_msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=Settings.SERVER_HOST,
        port=Settings.SERVER_PORT,
        log_level=Settings.LOG_LEVEL,
        reload=Settings.DEBUG_MODE,
    )
