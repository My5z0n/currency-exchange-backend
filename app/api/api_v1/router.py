from fastapi import APIRouter

from api.api_v1.endpoints.exchange_rate import router as exchange_rate_router
from api.api_v1.endpoints.currency import router as currency_router


router = APIRouter()

router.include_router(exchange_rate_router,
                      prefix="/exchanges", tags=["Exchange Rate"])
router.include_router(currency_router, prefix="/currency", tags=["Currency"])
