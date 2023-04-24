from api.models.requests import MajorDifferenceRequest
from api.models.responses import MajorDifferenceResponse
from api.services.currency_service import CurrencyService, get_currency_service
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get(
    "/major-difference/{currency_code}/{num_quotations}",
    response_model=MajorDifferenceResponse,
    name="currency:major_difference:get"
)
def get_major_difference_handler(request: MajorDifferenceRequest = Depends(), service: CurrencyService = Depends(get_currency_service)):
    """Get the major difference between the buy and ask rate for the given currency and number of quotations."""
    major_diff = service.get_major_diffrence(
        request.currency_code, request.num_quotations)
    return {major_diff}
