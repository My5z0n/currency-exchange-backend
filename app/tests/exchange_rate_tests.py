from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from datetime import date, timedelta
from api.services.currency_service import CurrencyService
from api.core.exceptions import NoDataError
from main import app


client = TestClient(app)


def test_get_exchange_rate_handler_success():
    # Mock the CurrencyService.get_exchange_rate method to return a valid exchange rate
    mock_service = MagicMock(spec=CurrencyService)
    mock_service.get_exchange_rate.return_value = 4.2855

    # Send a request to the API
    response = client.get("/api/v1/exchanges/USD/2023-04-04")

    # Verify the response is as expected
    assert response.status_code == 200
    assert response.json() == {
        "currency_code": "USD", "exchange_date": "2023-04-04", "average_exchange_rate": 4.2855}


def test_get_exchange_rate_handler_no_data():
    # Mock the CurrencyService.get_exchange_rate method to raise a NoDataError
    mock_service = MagicMock(spec=CurrencyService)
    mock_service.get_exchange_rate.side_effect = NoDataError("Data not found")

    # Send a request to the API
    response = client.get("/api/v1/exchanges/USD/2023-01-01")

    # Verify the response is as expected
    assert response.status_code == 404
    assert response.json() == {"message": "Data not found"}


def test_get_exchange_rate_handler_invalid_date():
    # Send a request to the API with an invalid date format
    response = client.get("/api/v1/exchanges/USD/20220101")

    # Verify the response is as expected
    assert response.status_code == 422
    assert response.json() == {"message": "Invalid Request"}


def test_get_exchange_rate_handler_invalid_currency():
    # Send a request to the API with an invalid currency code
    response = client.get("/api/v1/exchanges/INVALID/2023-01-01")

    # Verify the response is as expected
    assert response.status_code == 422
    assert response.json() == {"message": "Invalid Request"}


def test_get_exchange_rate_handler_future_date():
    # Send a request to the API with a future date
    tomorrow = date.today() + timedelta(1)
    response = client.get(
        f"/api/v1/exchanges/USD/{tomorrow.strftime('%Y-%m-%d')}")

    # Verify the response is as expected
    assert response.status_code == 422
    assert response.json() == {"message": "Invalid Request"}


def test_get_exchange_rate_handler_past_date():
    # Send a request to the API with a past date that is not available in the database
    response = client.get("/api/v1/exchanges/USD/2019-01-01")

    # Verify the response is as expected
    assert response.status_code == 404
    assert response.json() == {"message": "Data not found"}


def test_get_exchange_rate_handler_connection_error():
    # Mock the CurrencyService.get_exchange_rate method to raise a ConnectionError
    mock_service = MagicMock(spec=CurrencyService)
    mock_service.get_exchange_rate.side_effect = ConnectionError(
        "Unable to connect to server")

    # Send a request to the API
    response = client.get("/api/v1/exchanges/USD/2023-01-01")

    # Verify the response is as expected
    assert response.status_code == 503
    assert response.json() == {"message": "Service Unavailable"}


def test_get_exchange_rate_handler_timeout():
    # Mock the CurrencyService.get_exchange_rate method to raise a TimeoutError
    mock_service = MagicMock(spec=CurrencyService)
    mock_service.get_exchange_rate.side_effect = TimeoutError(
        "Connection timed out")

    # Send a request to the API
    response = client.get("/api/v1/exchanges/USD/2023-01-01")

    # Verify the response is as expected
    assert response.status_code == 504
    assert response.json() == {"message": "Gateway Timeout"}
