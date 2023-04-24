from fastapi import APIRouter

from api.api_v1.endpoints.exchange_rates_a import router as exchange_rate_router
from api.api_v1.endpoints.exchnage_rates_c import router as currency_router


router = APIRouter()

router.include_router(exchange_rate_router,
                      prefix="/exchange-rate/a", tags=["Exchange Rate A Table"])
router.include_router(
    currency_router, prefix="/exchange-rate/c", tags=["Exchange Rate C Table"])
