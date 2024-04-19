from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, conint, Extra


MIN_STR_LENGTH = 1
MAX_NAME_LENGTH = 100


class CharityProjectBase(BaseModel):
    name: str = Field(
        ...,
        min_length=MIN_STR_LENGTH,
        max_length=MAX_NAME_LENGTH
    )
    description: str = Field(..., min_length=MIN_STR_LENGTH)
    full_amount: conint(gt=0)  # type:ignore

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int = 0
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(
        None,
        min_length=MIN_STR_LENGTH,
        max_length=MAX_NAME_LENGTH
    )
    description: Optional[str] = Field(None, min_length=MIN_STR_LENGTH)
    full_amount: Optional[conint(gt=0)]  # type:ignore
