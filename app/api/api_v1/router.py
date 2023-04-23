from fastapi import APIRouter

from app.api.api_v1.endpoints.exchange_rate import router as exchange_rate_router
from app.api.api_v1.endpoints.currency import router as currency_router


router = APIRouter()

router.include_router(exchange_rate_router,
                      prefix="/exchange-rate", tags=["Exchange Rate"])
router.include_router(currency_router, prefix="/currency", tags=["Currency"])
