from typing import Annotated, Optional
from pydantic import Field, PositiveFloat
from fastapi_python.categoria.schemas import CategoriaIn
from fastapi_python.centro_treinamento.schemas import CentroTreinamentoAtleta
from datetime import datetime
# ajuda a fazer as validações
from fastapi_python.contrib.schemas import BaseSchema, OutMixin

class Atleta(BaseSchema):
    nome: Annotated[str, Field(description = 'nome do atleta', example='João', max_length=50)]
    cpf: Annotated[str, Field(description = 'cpf do atleta', example='09876543212', max_length=11)]
    idade: Annotated[int, Field(description = 'idade do atleta', example=25)]
    peso: Annotated[PositiveFloat, Field(description = 'peso do atleta', example=80.3)]
    altura: Annotated[PositiveFloat, Field(description = 'altura do atleta', example='1.70')]
    sexo: Annotated[str, Field(description = 'sexo do atleta', example='F', max_length=1)]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro de treinamento do atleta')]


class AtletaIn(Atleta):
    pass

class AtletaOutAll(Atleta, OutMixin):
    pass

class AtletaOutParcial(BaseSchema):
    nome: Annotated[str, Field(description='nome do atleta', example='João', max_length=50)]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro de treinamento do atleta')]


class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description='Nome do atleta', example='Joao', max_length=50)]
    idade: Annotated[Optional[int], Field(None, description='Idade do atleta', example=25)]