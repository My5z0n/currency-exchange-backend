from api.models.requests import ExchangeRateRequest, MaxMinAverageValueRequest
from api.models.responses import ExchangeRateResponse, MaxMinAverageValueResponse
from api.services.currency_service import CurrencyService, get_currency_service
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/{currency_code}/{exchange_date}", response_model=ExchangeRateResponse, name="exchange_rate:get")
def get_exchange_rate_handler(request: ExchangeRateRequest = Depends(), service: CurrencyService = Depends(get_currency_service)):
    """Get the average exchange rate for the given currency and date."""
    exchange_rate_result = service.get_exchange_rate(
        request.currency_code, request.exchange_date)
    exchange_rate_response = ExchangeRateResponse(
        currency_code=request.currency_code, exchange_date=request.exchange_date, average_exchange_rate=exchange_rate_result)
    return exchange_rate_response


@router.get(
    "/max-min-average/{currency_code}/{num_quotations}",
    response_model=MaxMinAverageValueResponse,
    name="currency:max_min_average:get"
)
def get_max_min_average_value_handler(request: MaxMinAverageValueRequest = Depends(), service: CurrencyService = Depends(get_currency_service)):
    """Get the max and min average value for the given currency and number of quotations."""
    min_max_result = service.get_max_min_average_value(
        request.currency_code, request.num_quotations)
    return min_max_result
