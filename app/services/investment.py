from typing import Union
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def invest(
    object: Union[Donation, CharityProject],
    session: AsyncSession
) -> Union[Donation, CharityProject]:
    """Iterates over all avaliable donations or charity projects and
    invests from donation or into project, if possible.
    """
    query_objects: list[Union[Donation, CharityProject]] = await (
        get_investment_objects(object, session)
    )
    if not query_objects:
        return object
    for item in query_objects:
        amount_to_invest = item.full_amount - item.invested_amount
        money_left = object.full_amount - object.invested_amount
        if amount_to_invest == money_left:
            close_investment(object)
            close_investment(item)
            session.add(item)
            break
        elif amount_to_invest > money_left:
            item.invested_amount += money_left
            close_investment(object)
            session.add(item)
            break
        else:
            close_investment(item)
            object.invested_amount += amount_to_invest
            session.add(item)
    session.add(object)
    await session.commit()
    await session.refresh(object)
    return object


async def get_investment_objects(
    object: Union[Donation, CharityProject],
    session: AsyncSession
) -> list[Union[Donation, CharityProject]]:
    """Returns all objects available for investments.
    Query model is the opposite of the incoming model:
    i.e. if Donation is in, list[CharityProject] is returned
    and vise versa.
    """
    query_model: Union[Donation, CharityProject] = (
        Donation if isinstance(object, CharityProject) else CharityProject
    )
    query_objects = await session.execute(
        select(query_model).where(
            query_model.fully_invested == False  # noqa
        )
    )
    return query_objects.scalars().all()


def close_investment(object: Union[Donation, CharityProject]):
    object.invested_amount = object.full_amount
    object.fully_invested = True
    object.close_date = datetime.now()
