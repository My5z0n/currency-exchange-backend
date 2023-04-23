import datetime

from fastapi import Depends
from api.core.exceptions import UserInputError
from api.repositories.currency_repository import CurrencyRepository, get_currency_repository


class CurrencyService():
    def __init__(self, currency_repository: CurrencyRepository) -> None:
        self.currency_repository = currency_repository

    def get_exchange_rate(self, currency_code: str, exchange_date: datetime.date) -> float:
        currency_code = currency_code.upper()
        currency_codes = self.currency_repository.get_table_currency_codes('a')
        if currency_code not in currency_codes:
            raise UserInputError(
                f"Currency code {currency_code} is not supported.")

        average_exchange_rate = self.currency_repository.get_average_exchange_rate(
            exchange_date, currency_code)
        return average_exchange_rate


def get_currency_service(currency_repository: CurrencyRepository = Depends(get_currency_repository)) -> CurrencyService:
    return CurrencyService(currency_repository)
