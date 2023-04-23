from datetime import date

from pydantic import BaseModel


class ExchangeRateResponse(BaseModel):
    currency_code: str  # 3-letter currency code, e.g. "GBP"
    exchange_date: date  # Date in YYYY-MM-DD format
    average_exchange_rate: float
