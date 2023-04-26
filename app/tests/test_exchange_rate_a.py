from datetime import date, timedelta
from unittest.mock import MagicMock

from api.core.exceptions import NoDataError
from api.models.repository import CurrencyRate
from api.models.responses import MaxMinAverageValueResponse
from api.repositories.currency_repository import CurrencyRepository
from api.services.currency_service import CurrencyService
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_exchange_rate_handler_success():
    # Mock the CurrencyService.get_exchange_rate method to return a valid exchange rate
    mock_service = MagicMock(spec=CurrencyService)
    mock_service.get_exchange_rate.return_value = 4.2855

    # Send a request to the API
    response = client.get("/api/v1/exchange-rate/a/USD/2023-04-04")

    # Verify the response is as expected
    assert response.status_code == 200
    assert response.json() == {
        "currency_code": "USD", "exchange_date": "2023-04-04", "average_exchange_rate": 4.2855}


def test_get_exchange_rate_handler_no_data():
    # Mock the CurrencyService.get_exchange_rate method to raise a NoDataError
    mock_service = MagicMock(spec=CurrencyService)
    mock_service.get_exchange_rate.side_effect = NoDataError("Data not found")

    # Send a request to the API
    response = client.get("/api/v1/exchange-rate/a/USD/2023-01-01")

    # Verify the response is as expected
    assert response.status_code == 404
    assert response.json() == {"message": "Data not found"}


def test_get_exchange_rate_handler_invalid_date():
    # Send a request to the API with an invalid date format
    response = client.get("/api/v1/exchange-rate/a/USD/20220101")

    # Verify the response is as expected
    assert response.status_code == 422
    assert response.json()["message"] == "Unprocessable Request"


def test_get_exchange_rate_handler_invalid_currency():
    # Send a request to the API with an invalid currency code
    response = client.get("/api/v1/exchange-rate/a/INVALID/2023-01-01")

    # Verify the response is as expected
    assert response.status_code == 422
    assert response.json()["message"] == "Unprocessable Request"


def test_get_exchange_rate_handler_future_date():
    # Send a request to the API with a future date
    tomorrow = date.today() + timedelta(1)
    response = client.get(
        f"/api/v1/exchange-rate/a/USD/{tomorrow.strftime('%Y-%m-%d')}")

    # Verify the response is as expected
    assert response.status_code == 422
    assert response.json()["message"] == "Unprocessable Request"


def test_get_exchange_rate_handler_past_date():
    # Send a request to the API with a past date that is not available in the database
    response = client.get("/api/v1/exchange-rate/a/USD/2019-01-01")

    # Verify the response is as expected
    assert response.status_code == 404
    assert response.json() == {"message": "Data not found"}


def test_get_max_min_average_value():
    mocked_currency_repository = MagicMock(spec=CurrencyRepository)
    currency_service = CurrencyService(mocked_currency_repository)

    # Mocked data
    currency_code = "USD"
    last_quotations = 10
    currency_rates = [
        CurrencyRate(date(2022, 4, 1), 1, 1.5),
        CurrencyRate(date(2022, 4, 2), 1, 1.2),
        CurrencyRate(date(2022, 4, 3), 1, 1.8),
        CurrencyRate(date(2022, 4, 4), 1, 1.6),
        CurrencyRate(date(2022, 4, 5), 1, 1.3),
        CurrencyRate(date(2022, 4, 6), 1, 1.7),
        CurrencyRate(date(2022, 4, 7), 1, 1.9),
        CurrencyRate(date(2022, 4, 8), 1, 1.4),
        CurrencyRate(date(2022, 4, 9), 1, 1.1),
        CurrencyRate(date(2022, 4, 10), 1, 1.0)
    ]

    # Set up mock
    mocked_currency_repository.get_last_n_rates_a_table.return_value = currency_rates

    # Expected result
    expected_result = MaxMinAverageValueResponse(
        currency_code=currency_code,
        span_begin_date=date(2022, 4, 1),
        span_end_date=date(2022, 4, 10),
        max_value=1.9,
        min_value=1.0
    )

    # Call the service method
    result = currency_service.get_max_min_average_value(
        currency_code, last_quotations)

    # Check the result
    assert result == expected_result
