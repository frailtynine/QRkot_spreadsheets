from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.donation import (
    DonationDB,
    DonationCreate,
    DonationByUser
)
from app.models.user import User
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.services.investment import invest

router = APIRouter()


@router.post(
    '/',
    response_model=DonationByUser
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Authentificated users only."""
    donation = await donation_crud.create(donation, session, user)
    return await invest(donation, session)


@router.get(
    '/my',
    response_model=list[DonationByUser]
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Authenticated users only."""
    return await donation_crud.get_by_user(user, session)


@router.get(
    '/',
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)]
)
async def get_all_user_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Superusers only."""
    return await donation_crud.get_multi(session)
