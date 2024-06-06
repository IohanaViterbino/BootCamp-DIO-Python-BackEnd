from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from fastapi_pagination import LimitOffsetPage, paginate
from sqlalchemy.exc import IntegrityError
from pydantic import UUID4
from fastapi_python.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from fastapi_python.centro_treinamento.models import CentroTreinamentoModel

from fastapi_python.contrib.dependencies import DatabaseDependency
from sqlalchemy.future import select

router = APIRouter()

@router.post(
    '/', 
    summary='Criar um novo Centro de treinamento',
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut,
)
async def post(
    db_session: DatabaseDependency, 
    centro_treinamento_in: CentroTreinamentoIn = Body(...)
) -> CentroTreinamentoOut:
    centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.model_dump())
    centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())
    try:
        db_session.add(centro_treinamento_model)
        await db_session.commit()
    
    except IntegrityError as e:    
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER, 
            detail=f'Já existe um atleta cadastrado com o cpf: {centro_treinamento_in.cpf}'
        )
    except Exception as e:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f'Ocorreu um erro ao inserir os dados no banco: {e}'
        )
    return centro_treinamento_out
    
    
@router.get(
    '/', 
    summary='Consultar todos os centros de treinamento',
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[CentroTreinamentoOut],
)
async def query(db_session: DatabaseDependency) -> LimitOffsetPage[CentroTreinamentoOut]:
    centros_treinamento_out: list[CentroTreinamentoOut] = (
        await db_session.execute(select(CentroTreinamentoModel))
    ).scalars().all()
    
    return paginate(centros_treinamento_out)


@router.get(
    '/{id}', 
    summary='Consulta um centro de treinamento pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> CentroTreinamentoOut:
    centro_treinamento_out: CentroTreinamentoOut = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
    ).scalars().first()

    if not centro_treinamento_out:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Centro de treinamento não encontrado no id: {id}'
        )
    
    return centro_treinamento_out