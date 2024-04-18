from datetime import datetime
from typing import Optional

from pydantic import BaseModel, conint


class DonationBase(BaseModel):
    full_amount: conint(gt=0)  # type:ignore
    comment: Optional[str]


class DonationCreate(DonationBase):
    pass


class DonationDB(DonationBase):
    id: int
    create_date: datetime
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class DonationByUser(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True
