from fastapi import Depends
import requests
from datetime import date
from api.core.config import config, Settings


class CurrencyRepository:
    def __init__(self, config: Settings) -> None:
        self.API_URL = config.API_URL

    def get_table_currency_codes(self, table_name) -> list[str]:
        url = f"{self.API_URL}/exchangerates/tables/{table_name}/?format=json"
        response = requests.get(url)
        response.raise_for_status()

        response_json = response.json()
        currency_codes = [rate['code'].upper()
                          for rate in response_json[0]['rates']]
        return currency_codes

    def get_average_exchange_rate(self, selected_date: date, currency: str) -> float:
        url = f"{self.API_URL}/exchangerates/rates/a/{currency}/{selected_date.strftime('%Y-%m-%d')}/?format=json"
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        rates = data['rates']
        average_rate = float(rates[0]['mid'])
        return average_rate


def get_currency_repository() -> CurrencyRepository:
    return CurrencyRepository(config)
