from datetime import date, datetime
from pydantic import BaseModel, validator
from fastapi import Path
from fastapi.exceptions import RequestValidationError
from api.core.exceptions import UserInputError


class ExchangeRateRequest(BaseModel):
    currency_code: str = Path(...,
                              regex=r"^[A-Za-z]{3}$", validate_assignment=True)
    exchange_date: date = Path(..., validate_assignment=True)

    @validator('exchange_date')
    def validate_exchange_date(cls, value):
        if value >= date.today():
            raise UserInputError("Exchange date must be older than today.")
        if value < date(2002, 1, 2):
            raise UserInputError(
                "Exchange date must be newer than 2002-01-02.")
        return value


class MaxMinAverageValueRequest(BaseModel):
    currency_code: str = Path(...,
                              regex=r"^[A-Za-z]{3}$", validate_assignment=True)
    num_quotations: int = Path(..., gt=0, le=255, validate_assignment=True)


class MajorDifferenceRequest(BaseModel):
    currency_code: str = Path(...,
                              regex=r"^[A-Za-z]{3}$", validate_assignment=True)
    num_quotations: int = Path(..., gt=0, le=255, validate_assignment=True)
