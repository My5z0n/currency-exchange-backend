from fastapi import FastAPI
from app.api.api_v1 import router as api_router_v1
from app.api.core.config import settings


def get_application() -> FastAPI:
    application = FastAPI(title="Python Backend NBP", debug=settings.DEBUG)
    application.include_router(api_router_v1, prefix="/api/v1")
    return application


app = get_application()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL,
        reload=settings.DEBUG,
    )
