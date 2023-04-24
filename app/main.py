from api.api_v1.router import router as api_router_v1
from api.core.config import config
from api.core.exception_handlers import get_exception_handlers
from fastapi import FastAPI


def get_application() -> FastAPI:
    application = FastAPI(title="Python Backend NBP",
                          debug=config.DEBUG_MODE, exception_handlers=get_exception_handlers())
    application.include_router(api_router_v1, prefix="/api/v1")
    return application


app = get_application()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        log_level=config.LOG_LEVEL,
        reload=config.DEBUG_MODE,
    )
