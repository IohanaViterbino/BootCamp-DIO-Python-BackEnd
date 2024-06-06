from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from fastapi_python.contrib.models import BaseModel


class CategoriaModel(BaseModel):
    __tablename__ = 'categorias'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(10), nullable=False)
    atleta: Mapped['AtletaModel'] = relationship(back_populates="categoria")