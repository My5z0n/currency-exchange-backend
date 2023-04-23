from fastapi import Depends
import requests
from datetime import date
from api.core.config import config, Settings
from api.core.exceptions import RepositoryError


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
        except requests.exceptions as e:
            raise RepositoryError(f"Error fetching currency codes: {e}")
        return currency_codes

    def get_average_exchange_rate(self, selected_date: date, currency: str) -> float:
        try:
            url = f"{self.API_URL}/exchangerates/rates/a/{currency}/{selected_date.strftime('%Y-%m-%d')}/?format=json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()
            rates = data['rates']
            average_rate = float(rates[0]['mid'])
        except requests.exceptions as e:
            raise RepositoryError(f"Error fetching exchange rate: {e}")
        return average_rate


def get_currency_repository() -> CurrencyRepository:
    return CurrencyRepository(config)
