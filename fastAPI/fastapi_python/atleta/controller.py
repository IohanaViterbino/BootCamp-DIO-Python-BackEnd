from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from sqlalchemy.exc import IntegrityError
from pydantic import UUID4
from fastapi_pagination import LimitOffsetPage, paginate

from fastapi_python.atleta.schemas import AtletaIn, AtletaOutAll, AtletaOutParcial, AtletaUpdate
from fastapi_python.atleta.models import AtletaModel
from fastapi_python.categoria.models import CategoriaModel
from fastapi_python.centro_treinamento.models import CentroTreinamentoModel

from fastapi_python.contrib.dependencies import DatabaseDependency
from sqlalchemy.future import select

router = APIRouter()

@router.post(
    '/', 
    summary='Criar um novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOutAll
)
async def post(
    db_session: DatabaseDependency, 
    atleta_in: AtletaIn = Body(...)
):
    categoria_nome = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome

    categoria = (await db_session.execute(
        select(CategoriaModel).filter_by(nome=categoria_nome))
    ).scalars().first()
    
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f'A categoria {categoria_nome} não foi encontrada.'
        )
    
    centro_treinamento = (await db_session.execute(
        select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome))
    ).scalars().first()
    
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f'O centro de treinamento {centro_treinamento_nome} não foi encontrado.'
        )
    try:
        atleta_out = AtletaOutAll(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))

        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
        
        db_session.add(atleta_model)
        await db_session.commit()

    except IntegrityError as e:    
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER, 
            detail=f'Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}'
        )
    except Exception as e:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f'Ocorreu um erro ao inserir os dados no banco: {e}'
        )
    return atleta_out

@router.get(
    '/', 
    summary='Consultar todos os Atletas',
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[AtletaOutParcial],
)
async def query(db_session: DatabaseDependency) -> LimitOffsetPage[AtletaOutParcial]:
    result = await db_session.execute(
        select(
            AtletaModel.nome,
            CategoriaModel.nome.label('categoria_nome'),
            CentroTreinamentoModel.nome.label('centro_treinamento_nome')
        ).join(CategoriaModel, AtletaModel.categoria_id == CategoriaModel.pk_id)
         .join(CentroTreinamentoModel, AtletaModel.centro_treinamento_id == CentroTreinamentoModel.pk_id)
    )
    rows = result.all()

    # Convertendo as linhas em dicionários
    atletas = [
        {
            'nome': row.nome,
            'categoria': {'nome': row.categoria_nome},
            'centro_treinamento': {'nome': row.centro_treinamento_nome}
        }
        for row in rows
    ]

    # Convertendo os dicionários para os modelos de saída
    atletas_out = [AtletaOutParcial.model_validate(atleta) for atleta in atletas]

    # Paginação dos resultados
    return paginate(atletas_out)

# trocar por id para cpf
@router.get(
    '/{cpf}', 
    summary='Consulta um Atleta pelo cpf',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOutAll,
)
async def get(cpf: str, db_session: DatabaseDependency) -> AtletaOutAll:
    atleta: AtletaOutAll = (
        await db_session.execute(select(AtletaModel).filter_by(cpf=cpf))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta não encontrado com cpf: {cpf}'
        )
    
    return atleta

@router.patch(
    '/{cpf}', 
    summary='Editar um Atleta pelo cpf',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOutAll,
)
async def patch(cpf: str, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOutAll:
    atleta: AtletaOutAll = (
        await db_session.execute(select(AtletaModel).filter_by(cpf=cpf))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta não encontrado com cpf: {cpf}'
        )
    try:
        atleta_update = atleta_up.model_dump(exclude_unset=True)
        for key, value in atleta_update.items():
            setattr(atleta, key, value)

        await db_session.commit()
        await db_session.refresh(atleta)

    except IntegrityError as e:    
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER, 
            detail=f'Já existe um atleta cadastrado com o cpf: {atleta_up.cpf}'
        )
    except Exception as e:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f'Ocorreu um erro ao inserir os dados no banco: {e}'
        )
    
    return atleta


@router.delete(
    '/{cpf}', 
    summary='Deletar um Atleta pelo cpf',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(cpf: str, db_session: DatabaseDependency) -> None:
    atleta: AtletaOutAll = (
        await db_session.execute(select(AtletaModel).filter_by(cpf=cpf))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta não encontrado com cpf: {cpf}'
        )
    
    await db_session.delete(atleta)
    await db_session.commit()