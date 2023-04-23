import datetime

from api.models.requests import ExchangeRateRequest
from api.models.responses import ExchangeRateResponse
from fastapi import APIRouter, Depends
from api.services.currency_service import get_currency_service, CurrencyService

router = APIRouter()


@router.get("/{currency_code}/{exchange_date}", response_model=ExchangeRateResponse, name="exchange_rate:get")
def get_exchange_rate_handler(request: ExchangeRateRequest = Depends(), service: CurrencyService = Depends(get_currency_service)):
    """Get the average exchange rate for the given currency and date."""
    exchange_rate_result = service.get_exchange_rate(
        request.currency_code, request.exchange_date)
    exchange_rate_response = ExchangeRateResponse(
        currency_code=request.currency_code, exchange_date=request.exchange_date, average_exchange_rate=exchange_rate_result)
    return exchange_rate_response
