from typing import Annotated

from pydantic import UUID4, Field
from workout_api.categorias.models import CategoriaModel
from workout_api.contrib.schemas import BaseSchema


class CategoriaIn(BaseSchema):
    nome: Annotated[
        str, Field(description="Nome da categoria", example="Legs", max_length=10)
    ]


class CategoriaOut(CategoriaIn):
    id: Annotated[UUID4, Field(description="Id do registro")]


breakpoint()
pass
