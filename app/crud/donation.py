from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.core.user import User


class CRUDDonationBase(CRUDBase):
    async def get_by_user(
        self,
        user: User,
        session: AsyncSession
    ) -> list[Donation]:
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()


donation_crud = CRUDDonationBase(Donation)
