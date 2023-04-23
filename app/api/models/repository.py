from dataclasses import dataclass
from datetime import date


@dataclass
class ACurrencyRate:
    date: date
    number: int
    rate: float


@dataclass
class CCurrencyRate:
    date: date
    number: int
    bid: float
    ask: float
