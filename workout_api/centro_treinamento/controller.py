from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy import select

from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.centro_treinamento.schemas import (
    CentroTreinamentoIn,
    CentroTreinamentoOut,
)
from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter()


@router.post(
    "/",
    summary="Cria um novo centro de treinamento",
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut,
)
async def post(
    db_session: DatabaseDependency,
    centro_treinamento_in: CentroTreinamentoIn = Body(...),
) -> CentroTreinamentoOut:

    centro_treinamento_out = CentroTreinamentoOut(
        id=UUID4(), **CentroTreinamentoIn.model_dump()
    )
    centro_treinamento_model = CentroTreinamentoModel(
        **centro_treinamento_out.model_dump()
    )

    db_session.add(centro_treinamento_model)
    await db_session.commit()
    return centro_treinamento_out


@router.get(
    "/",
    summary="consulta todos os centros de treinamento",
    status_code=status.HTTP_200_OK,
    response_model=list[CentroTreinamentoOut],
)
async def query(
    db_session: DatabaseDependency,
    centro_treinamento_in: CentroTreinamentoIn = Body(...),
) -> list[CentroTreinamentoOut]:
    centro_treinamento: list[CentroTreinamentoOut] = await db_session.execute(
        select(CentroTreinamentoModel).scalars().all()
    )
    return centro_treinamento


@router.get(
    "/{id}",
    summary="consulta centro treianmento por id",
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def query(
    id: UUID4,
    db_session: DatabaseDependency,
    centro_treinamento_in: CentroTreinamentoIn = Body(...),
) -> CentroTreinamentoOut:
    centro_treinamento: CentroTreinamentoOut = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
        .scalars()
        .first()
    )

    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    return centro_treinamento
