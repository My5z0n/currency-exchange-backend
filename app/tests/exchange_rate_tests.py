from fastapi.testclient import TestClient
from unittest.mock import MagicMock
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
