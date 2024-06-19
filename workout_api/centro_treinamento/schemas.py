from typing import Annotated

from pydantic import UUID4, Field
from workout_api.contrib.schemas import BaseSchema


class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[
        str,
        Field(
            description="Nome do centro de treinamento",
            example="CT kings",
            max_length=20,
        ),
    ]
    endereco: Annotated[
        str,
        Field(
            description="Endereço do centro de treinamento",
            example="rua dos bobos",
            max_length=60,
        ),
    ]
    proprietario: Annotated[
        str, Field(description="nome do proprietário", example="Marcos", max_length=30)
    ]


class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[
        str,
        Field(
            description="niome do centro de treinamento",
            exammple="CT kings",
            max_length=20,
        ),
    ]


class CentroTreinamentoOut(CentroTreinamentoIn):
    id: Annotated[UUID4, Field(description="Id do registro")]
