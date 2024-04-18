from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate
from app.crud.charity_project import charity_project_crud


async def check_project_status_before_delete(
    project_id: CharityProject,
    session: AsyncSession
) -> CharityProject:
    charity_project: CharityProject = await charity_project_crud.get(
        project_id,
        session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден'
        )
    if charity_project.close_date:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя удалить закрытый проект!'
        )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return charity_project


async def check_project_before_edit(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession
) -> CharityProject:
    charity_project: CharityProject = await charity_project_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден'
        )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект закрыт и не может быть обновлен.'
        )
    if obj_in.full_amount and obj_in.full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя установить значение full_amount меньше уже вложенной суммы.'
        )
    if obj_in.name:
        charity_project_same_name = (
            await charity_project_crud.get_project_by_name(
                obj_in.name,
                session
            )
        )
        if (
            charity_project_same_name is not None and
            obj_in.name != charity_project.name
        ):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST
            )
    return charity_project


async def check_project_name_dublicate(
    project_name: str,
    session: AsyncSession
) -> None:
    project = await charity_project_crud.get_project_by_name(
        project_name,
        session
    )
    if project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )
