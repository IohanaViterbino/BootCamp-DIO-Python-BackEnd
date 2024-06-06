from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from fastapi_pagination import LimitOffsetPage, paginate
from sqlalchemy.exc import IntegrityError
from pydantic import UUID4
from fastapi_python.categoria.schemas import CategoriaIn, CategoriaOut
from fastapi_python.categoria.models import CategoriaModel

from fastapi_python.contrib.dependencies import DatabaseDependency
from sqlalchemy.future import select

router = APIRouter()

@router.post(
    '/', 
    summary='Criar uma nova Categoria',
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut,
)
async def post(
    db_session: DatabaseDependency, 
    categoria_in: CategoriaIn = Body(...)
) -> CategoriaOut:
    categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())
    try:
        db_session.add(categoria_model)
        await db_session.commit()
    
    except IntegrityError as e:    
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER, 
            detail=f'Já existe um atleta cadastrado com o cpf: {categoria_in.cpf}'
        )
    except Exception as e:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f'Ocorreu um erro ao inserir os dados no banco: {e}'
        )
    return categoria_out

    
@router.get(
    '/', 
    summary='Consultar todas as Categorias',
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[CategoriaOut],
)
async def query(db_session: DatabaseDependency) -> LimitOffsetPage[CategoriaOut]:
    categorias: list[CategoriaOut] = (await db_session.execute(select(CategoriaModel))).scalars().all()
    
    return paginate(categorias)


@router.get(
    '/{id}', 
    summary='Consulta uma Categoria pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> CategoriaOut:
    categoria: CategoriaOut = (
        await db_session.execute(select(CategoriaModel).filter_by(id=id))
    ).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Categoria não encontrada no id: {id}'
        )
    
    return categoria