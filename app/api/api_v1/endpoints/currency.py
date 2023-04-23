from fastapi import APIRouter, Depends
from api.models.requests import MaxMinAverageValueRequest, MajorDifferenceRequest
from api.models.responses import MaxMinAverageValueResponse, MajorDifferenceResponse
from app.api.services.currency_service import get_currency_service, CurrencyService

router = APIRouter()


@ router.get(
    "/max-min-average/{currency_code}/{num_quotations}",
    response_model=MaxMinAverageValueResponse,
    name="currency:max_min_average:get"
)
def get_max_min_average_value_handler(request: MaxMinAverageValueRequest = Depends(), service: CurrencyService = Depends(get_currency_service)):
    """Get the max and min average value for the given currency and number of quotations."""
    min_max_result = service.get_max_min_average_value(
        request.currency_code, request.num_quotations)
    return min_max_result


@ router.get(
    "/major-difference/{currency_code}/{num_quotations}}",
    response_model=MajorDifferenceResponse,
    name="currency:major_difference:get"
)
def get_major_difference_handler(request: MajorDifferenceRequest = Depends(), service: CurrencyService = Depends(get_currency_service)):
    """Get the major difference between the buy and ask rate for the given currency and number of quotations."""
    major_diff = service.get_major_diffrence(
        request.currency_code, request.num_quotations)
    return {"major_diff": major_diff}
