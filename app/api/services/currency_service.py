import datetime

from fastapi import Depends
from api.core.exceptions import UserInputError
from api.repositories.currency_repository import CurrencyRepository, get_currency_repository
from app.api.models.responses import MajorDifferenceResponse, MaxMinAverageValueResponse


class CurrencyService():
    def __init__(self, currency_repository: CurrencyRepository) -> None:
        self.currency_repository = currency_repository

    def get_exchange_rate(self, currency_code: str, exchange_date: datetime.date) -> float:
        currency_code = currency_code.upper()
        currency_codes = self.currency_repository.get_table_currency_codes('a')
        if currency_code not in currency_codes:
            raise UserInputError(
                f"Currency code {currency_code} is not supported.")

        average_exchange_rate = self.currency_repository.get_average_exchange_rate_a_table(
            exchange_date, currency_code)
        return average_exchange_rate

    def get_max_min_average_value(self, currency_code: str, last_quotations: int) -> MaxMinAverageValueResponse:
        currency_rates = self.currency_repository.get_last_n_rates_a_table(
            currency_code, last_quotations)
        oldest_date = min(currency_rates, key=lambda x: x.effective_date).date
        newest_date = max(currency_rates, key=lambda x: x.effective_date).date
        rates = [rate.rate for rate in currency_rates]
        min_rate = min(rates)
        max_rate = max(rates)
        return MaxMinAverageValueResponse(currency_code=currency_code, start_date=oldest_date, end_date=newest_date, max_value=max_rate, min_value=min_rate)

    def get_major_diffrence(self, currency_code: str, last_quotations: int) -> MajorDifferenceResponse:
        currency_rates = self.currency_repository.get_last_n_rates_c_table(
            currency_code, last_quotations)
        oldest_date = min(currency_rates, key=lambda x: x.effective_date).date
        newest_date = max(currency_rates, key=lambda x: x.effective_date).date
        rates = [(rate.date, abs(rate.ask-rate.bid))
                 for rate in currency_rates]
        max_diff_date, max_diff_value = max(rates, key=lambda x: x[1])
        return MajorDifferenceResponse(currency_code=currency_code, start_date=oldest_date, end_date=newest_date, major_diffrence_value=max_diff_value, major_diffrence_date=max_diff_date)


def get_currency_service(currency_repository: CurrencyRepository = Depends(get_currency_repository)) -> CurrencyService:
    return CurrencyService(currency_repository)
