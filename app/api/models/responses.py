from datetime import date

from pydantic import BaseModel


class ExchangeRateResponse(BaseModel):
    currency_code: str              # 3-letter currency code, e.g. "GBP"
    exchange_date: date             # Date in YYYY-MM-DD format
    average_exchange_rate: float    # value of the average exchange rate


class MaxMinAverageValueResponse(BaseModel):
    currency_code: str      # 3-letter currency code, e.g. "GBP"
    span_begin_date: date   # Date in YYYY-MM-DD format
    span_end_date: date     # Date in YYYY-MM-DD format
    max_value: float        # Max value of the average exchange rate
    min_value: float        # Min value of the average exchange rate


class MajorDifferenceResponse(BaseModel):
    currency_code: str              # 3-letter currency code, e.g. "GBP"
    span_begin_date: date           # Date in YYYY-MM-DD format
    span_end_date: date             # Date in YYYY-MM-DD format
    major_diffrence_date: date      # Max value of the average exchange rate
    major_diffrence_value: float    # Max value of the average exchange rate
    ask_rate: float                 # Bid rate
    bid_rate: float                 # Buy rate
