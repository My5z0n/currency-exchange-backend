from api.api_v1.router import router as api_router_v1
from api.core.config import Settings
from api.core.exception_handlers import get_exception_handlers
from fastapi import FastAPI


def get_application() -> FastAPI:
    application = FastAPI(title="Python Backend NBP",
                          debug=Settings.DEBUG_MODE, exception_handlers=get_exception_handlers())
    application.include_router(api_router_v1, prefix="/api/v1")
    return application


app = get_application()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=Settings.SERVER_HOST,
        port=Settings.SERVER_PORT,
        log_level=Settings.LOG_LEVEL,
        reload=Settings.DEBUG_MODE,
    )
