import datetime
from unittest.mock import MagicMock

from api.models.responses import MajorDifferenceResponse
from api.repositories.currency_repository import CurrencyRateCTable
from api.services.currency_service import CurrencyService


def test_get_major_difference_returns_expected_response():
    # arrange
    currency_code = "USD"
    num_quotations = 5
    currency_rates = [
        CurrencyRateCTable(date=datetime.date(2022, 1, 1),
                           number=1, bid=1.0, ask=1.1),
        CurrencyRateCTable(date=datetime.date(2022, 1, 2),
                           number=2, bid=1.2, ask=1.4),
        CurrencyRateCTable(date=datetime.date(2022, 1, 3),
                           number=3, bid=1.4, ask=1.2),
        CurrencyRateCTable(date=datetime.date(2022, 1, 4),
                           number=4, bid=1.0, ask=1.9),
        CurrencyRateCTable(date=datetime.date(2022, 1, 5),
                           number=5, bid=1.6, ask=1.9),
    ]
    mock_repository = MagicMock()
    mock_repository.get_last_n_rates_c_table.return_value = currency_rates
    service = CurrencyService(mock_repository)

    # act
    response = service.get_major_diffrence(currency_code, num_quotations)

    # assert
    expected_response = MajorDifferenceResponse(
        currency_code=currency_code,
        span_begin_date=datetime.date(2022, 1, 1),
        span_end_date=datetime.date(2022, 1, 5),
        major_diffrence_date=datetime.date(2022, 1, 4),
        major_diffrence_value=0.9,
        ask_rate=1.9,
        bid_rate=1.0
    )
    assert response == expected_response
