from datetime import datetime
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy import select

from workout_api.atelta.models import AtletaModel
from workout_api.atelta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter()


@router.post(
    "/",
    summary="Cria um novo atleta",
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
)
async def post(db_session: DatabaseDependency, atleta_in: AtletaIn = Body(...)):
    categoria_nome = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome
    categoria = (
        (
            await db_session.execute(
                select(CategoriaModel).filter_by(nome=categoria.nome)
            )
        )
        .scalars()
        .first()
    )

    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")

    centro_treinamento = (
        (
            await db_session.execute(
                select(CentroTreinamentoModel).filter_by(nome=centro_treinamento.nome)
            )
        )
        .scalars()
        .first()
    )

    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    try:
        atleta_out = AtletaOut(
            id=UUID4(), created_at=datetime.now(), **atleta_in.model_dump()
        )

        atleta_model = AtletaModel(
            **atleta_out.model_dump(exclude={"categoria", "centro_treinamento"})
        )
        atleta_model.categoria_id = atleta_in.categoria.pk_id
        atleta_model.centro_treinamento_id = atleta_in.centro_treinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="internal server error",
        )
    return atleta_out


@router.get(
    "/",
    summary="consulta todos os atletas",
    status_code=status.HTTP_200_OK,
    response_model=list[AtletaOut],
)
async def query(db_session: DatabaseDependency) -> list[AtletaOut]:
    atletas: list[AtletaOut] = await db_session.execute(
        select(AtletaModel).scalars().all()
    )
    return [AtletaOut.model_validate(atleta) for atleta in atletas]


@router.get(
    "/{id}",
    summary="consulta um atleta",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    atleta = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalars()
        .first()
    )
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    return AtletaOut.model_validate(atleta)


@router.patch(
    "/{id}",
    summary="atualiza um atleta",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def patch(
    id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)
) -> AtletaOut:
    atleta = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalars()
        .first()
    )
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    atleta_uptade = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_up.itens():
        setattr(atleta, key, value)
    await db_session.commit()
    await db_session.refresh(atleta)
    return atleta


@router.delete(
    "/{id}", summary="deleta um atleta", status_code=status.HTTP_204_NO_CONTENT
)
async def delete(id: UUID4, db_session: DatabaseDependency):
    atleta = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalars()
        .first()
    )
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    await db_session.delete(atleta)
    await db_session.commit()
