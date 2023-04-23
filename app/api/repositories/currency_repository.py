from fastapi import Depends
import requests
from datetime import date
from api.core.config import config, Settings
from api.core.exceptions import RepositoryError
from api.core.exceptions import NoDataError


class CurrencyRepository:
    def __init__(self, config: Settings) -> None:
        self.API_URL = config.API_URL

    def get_table_currency_codes(self, table_name) -> list[str]:
        try:
            url = f"{self.API_URL}/exchangerates/tables/{table_name}/?format=json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            response_json = response.json()
            currency_codes = [rate['code'].upper()
                              for rate in response_json[0]['rates']]
            return currency_codes
        except requests.exceptions.HTTPError as http_error:
            if http_error.response.status_code == 404:
                raise NoDataError("Data not found.")
            else:
                raise RepositoryError(
                    f"Error fetching currency codes: {http_error}")
        except requests.exceptions as request_error:
            raise RepositoryError(
                f"Error fetching currency codes: {request_error}")

    def get_average_exchange_rate(self, selected_date: date, currency: str) -> float:
        try:
            url = f"{self.API_URL}/exchangerates/rates/a/{currency}/{selected_date.strftime('%Y-%m-%d')}/?format=json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()
            rates = data['rates']
            return float(rates[0]['mid'])
        except requests.exceptions.HTTPError as http_error:
            if http_error.response.status_code == 404:
                raise NoDataError("Data not found.")
            else:
                raise RepositoryError(
                    f"Error fetching exchange rate:: {http_error}")
        except requests.exceptions as request_error:
            raise RepositoryError(
                f"Error fetching currency codes: {request_error}")


def get_currency_repository() -> CurrencyRepository:
    return CurrencyRepository(config)
