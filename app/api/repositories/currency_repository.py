from datetime import date

import requests
from api.core.config import Settings, config
from api.core.exceptions import NoDataError, RepositoryError
from api.models.repository import CurrencyRate, CurrencyRateCTable


def handle_request_error(func):
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            return response
        except requests.exceptions.HTTPError as http_error:
            if http_error.response.status_code == 404:
                raise NoDataError("Data not found.")
            else:
                raise RepositoryError(f"Error fetching data: {http_error}")
        except requests.exceptions.RequestException as request_error:
            raise RepositoryError(f"Error fetching data: {request_error}")
        except Exception as ex:
            raise RepositoryError(f"Error occurred during parsing data: {ex}")
    return wrapper


class CurrencyRepository:
    def __init__(self, config: Settings) -> None:
        self.API_URL = config.API_URL

    @handle_request_error
    def get_table_currency_codes(self, table_name: str) -> list[str]:
        url = f"{self.API_URL}/exchangerates/tables/{table_name}/?format=json"

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        response_json = response.json()
        currency_codes = [rate['code'].upper()
                          for rate in response_json[0]['rates']]
        return currency_codes

    @handle_request_error
    def get_average_exchange_rate_a_table(self, selected_date: date, currency: str) -> float:
        url = f"{self.API_URL}/exchangerates/rates/a/{currency}/{selected_date.strftime('%Y-%m-%d')}/?format=json"

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        rates = data['rates']
        return float(rates[0]['mid'])

    @handle_request_error
    def get_last_n_rates_a_table(self, currency: str, num_days: int) -> list[CurrencyRate]:
        url = f"{self.API_URL}/exchangerates/rates/a/{currency}/last/{num_days}/?format=json"

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        rates = data['rates']
        currency_rates = [CurrencyRate(
            date=rate['effectiveDate'], number=rate['no'], rate=float(rate['mid'])) for rate in rates]
        return currency_rates

    @handle_request_error
    def get_last_n_rates_c_table(self, currency: str, num_days: int) -> list[CurrencyRateCTable]:
        url = f"{self.API_URL}/exchangerates/rates/c/{currency}/last/{num_days}/?format=json"

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        rates = data['rates']
        currency_rates = [CurrencyRateCTable(
            date=rate['effectiveDate'], number=rate['no'], bid=float(rate['bid']), ask=float(rate['ask'])) for rate in rates]
        return currency_rates


def get_currency_repository() -> CurrencyRepository:
    return CurrencyRepository(config)
