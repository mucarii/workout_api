from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from workout_api.atelta.models import AtletaModel
from workout_api.contrib.models import BaseModel


class CentroTreinamentoModel(BaseModel):
    __tablename__ = "centro_treinamento"
    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    endereco: Mapped[str] = mapped_column(String(60), nullable=False)
    propietario: Mapped[str] = mapped_column(String(30), nullable=False)
    categoria: Mapped["AtletaModel"] = relationship(back_populates="centro_treinamento")
