from typing import Union

from sqlalchemy import select, extract
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


SECONDS_IN_DAY = 86400


class CharityProjectCRUD(CRUDBase):
    async def get_project_by_name(
            self,
            obj_name: str,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.name == obj_name
            )
        )
        return db_obj.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ) -> list[dict[str, Union[str, int]]]:
        projects = await session.execute(
            select([
                self.model.name,
                (
                    (
                        extract(
                            'epoch', self.model.close_date
                        ) -
                        extract(
                            'epoch',
                            self.model.create_date
                        )
                    ) / SECONDS_IN_DAY
                ).label('completion_days'),
                self.model.description
            ]).where(
                self.model.fully_invested == True # noqa
            ).order_by(
                'completion_days'
            )
        )
        return projects.all()


charity_project_crud = CharityProjectCRUD(CharityProject)
