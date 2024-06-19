from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy import select

from workout_api.categorias.models import CategoriaModel
from workout_api.categorias.schemas import CategoriaIn, CategoriaOut
from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter()


@router.post(
    "/",
    summary="Cria uma nova categoria",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut,
)
async def post(
    db_session: DatabaseDependency, categoria_in: CategoriaIn = Body(...)
) -> CategoriaOut:

    categoria_out = CategoriaOut(id=UUID4(), **CategoriaIn.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())

    db_session.add(categoria_model)
    await db_session.commit()
    return categoria_out


@router.get(
    "/",
    summary="consulta todas as categorias",
    status_code=status.HTTP_200_OK,
    response_model=list[CategoriaOut],
)
async def query(
    db_session: DatabaseDependency, categoria_in: CategoriaIn = Body(...)
) -> list[CategoriaOut]:
    categorias: list[CategoriaOut] = await db_session.execute(
        select(CategoriaModel).scalars().all()
    )
    return categorias


@router.get(
    "/{id}",
    summary="consulta categoria por id",
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def query(
    id: UUID4, db_session: DatabaseDependency, categoria_in: CategoriaIn = Body(...)
) -> CategoriaOut:
    categoria: CategoriaOut = (
        await db_session.execute(select(CategoriaModel).filter_by(id=id))
        .scalars()
        .first()
    )

    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    return categoria
