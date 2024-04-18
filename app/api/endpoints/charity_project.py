from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate
)
from app.crud.charity_project import charity_project_crud
from app.core.user import current_superuser
from app.api.endpoints.validators import (
    check_project_status_before_delete,
    check_project_before_edit,
    check_project_name_dublicate
)
from app.services.investment import invest


router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB]
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Superuser only!"""
    await check_project_name_dublicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    return await invest(new_project, session)


@router.delete(
    '/{project_id}',
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Superuser only"""
    charity_project = await check_project_status_before_delete(project_id, session)
    return await charity_project_crud.remove(charity_project, session)


@router.patch(
    '/{project_id}',
    dependencies=[Depends(current_superuser)],
    response_model=CharityProjectDB,
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_project_before_edit(project_id, obj_in, session)
    charity_project = await charity_project_crud.update(charity_project, obj_in, session)
    return await invest(charity_project, session)
