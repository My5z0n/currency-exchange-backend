from dataclasses import dataclass
from datetime import date


@dataclass
class CurrencyRate:
    date: date
    number: int
    rate: float


@dataclass
class CurrencyRateCTable:
    date: date
    number: int
    bid: float
    ask: float
