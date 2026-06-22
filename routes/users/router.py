from fastapi import APIRouter, Depends, HTTPException, Path, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from database import get_db
from entities.user import User


router = APIRouter(prefix="/users", tags=["users"])


class UserCreate(BaseModel):
    name: str
    email: str
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Maria Silva",
                "email": "maria.silva@email.com",
                "password": "senhaSegura123",
            }
        }
    }


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
    is_active: bool | None = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Maria Silva",
                "email": "maria.silva@email.com",
                "password": "senhaSegura123",
                "is_active": True,
            }
        }
    }


def user_to_dict(user: User) -> dict:
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "password": user.password,
        "is_active": user.is_active,
        "created_at": str(user.created_at),
        "updated_at": str(user.updated_at),
    }


def erro(msg: str, status_code: int = 400) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "ok": False,
            "erro": msg,
            "status": status_code,
            "comentario": "Nao foi possivel concluir a requisicao.",
        },
    )


# POST /users/ -> cria um usuario apos validar nome, email, senha e duplicidade.
@router.post(
    "/",
    summary="Cria um novo usuario",
    description="Cadastra um novo usuario no banco de dados apos validar os dados enviados.",
)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    """
    Cria um novo usuario no banco de dados.

    Regras de validacao aplicadas antes de salvar:
    - `name`: obrigatorio e com no minimo 3 caracteres.
    - `email`: obrigatorio e precisa conter `@`. E armazenado em minusculas.
    - `password`: obrigatorio e nao pode ser vazio.
    - Nao pode existir outro usuario cadastrado com o mesmo `email`.

    Exemplo pre-definido para teste no Swagger:
    - name = "Maria Silva"
    - email = "maria.silva@email.com"
    - password = "senhaSegura123"

    Retorna os dados do usuario criado em caso de sucesso ou um erro de
    validacao (`422`) / conflito (`409`) quando os dados sao invalidos.
    """
    if len(payload.name) < 3:
        return erro("nome muito curto; informe ao menos 3 caracteres", 422)

    if "@" not in payload.email:
        return erro("email invalido; o caractere @ esta faltando", 422)

    if payload.password == "":
        return erro("senha obrigatoria; informe uma senha valida", 422)

    duplicated = db.scalar(select(User).where(User.email == payload.email.lower()))
    if duplicated:
        return erro("ja existe um usuario cadastrado com esse email", 409)

    user = User(
        name=payload.name,
        email=payload.email.lower(),
        password=payload.password,
    )
    db.add(user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return erro("nao foi possivel salvar o usuario no banco de dados", 500)

    db.refresh(user)
    return {
        "message": "Usuario criado com sucesso.",
        "data": user_to_dict(user),
    }


# GET /users/ -> lista os usuarios com paginacao (skip/limit).
@router.get("/")
def list_users(
    skip: int = Query(
        default=0,
        examples=[0],
        description="Quantos usuarios pular antes de comecar a listar (paginacao).",
    ),
    limit: int = Query(
        default=100,
        examples=[10],
        description="Numero maximo de usuarios retornados na resposta.",
    ),
    db: Session = Depends(get_db),
):
    """
    Lista os usuarios cadastrados no banco de dados.

    Usa paginacao simples atraves dos parametros `skip` (quantos registros pular)
    e `limit` (quantidade maxima a retornar). Por padrao retorna ate 100 usuarios
    a partir do primeiro registro.

    Exemplo pre-definido para teste no Swagger:
    - skip = 0
    - limit = 10

    Esse exemplo retorna os 10 primeiros usuarios cadastrados, sem pular nenhum.
    """
    users = db.scalars(select(User).offset(skip).limit(limit)).all()
    return {
        "message": "Lista entregue; mandei todos os dados como o senior pediu.",
        "total": len(users),
        "data": [user_to_dict(user) for user in users],
    }


# GET /users/{user_id} -> retorna um usuario pelo ID (404 se nao existir).
@router.get(
    "/{user_id}",
    summary="Busca um usuario por ID",
    description="Retorna os dados do usuario correspondente ao `user_id` informado.",
)
def get_user(
    user_id: int = Path(
        ...,
        examples=[1],
        description="ID do usuario que sera consultado.",
    ),
    db: Session = Depends(get_db),
):
    """
    Busca um unico usuario no banco de dados pelo seu ID.

    Recebe o `user_id` pela URL e retorna os dados do usuario correspondente.

    Exemplo pre-definido para teste no Swagger:
    - user_id = 1

    Retorna os dados do usuario em caso de sucesso ou um erro 404 quando o
    usuario informado nao existe.
    """
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        return erro("usuario nao encontrado", 404)

    return {
        "message": "Usuario encontrado com sucesso.",
        "data": user_to_dict(user),
    }


# PATCH /users/{user_id} -> atualizacao parcial; altera apenas os campos enviados.
@router.patch(
    "/{user_id}",
    summary="Atualiza um usuario",
    description="Atualiza parcialmente os dados do usuario correspondente ao `user_id` informado.",
)
def update_user(
    user_id: int = Path(
        ...,
        examples=[1],
        description="ID do usuario que sera atualizado.",
    ),
    payload: UserUpdate = ...,
    db: Session = Depends(get_db),
):
    """
    Atualiza parcialmente um usuario existente no banco de dados.

    Apenas os campos enviados no corpo da requisicao sao alterados; os demais
    permanecem com os valores atuais.

    Campos opcionais aceitos:
    - `name`: novo nome do usuario.
    - `email`: novo email do usuario.
    - `password`: nova senha do usuario.
    - `is_active`: define se o usuario esta ativo (`true`) ou inativo (`false`).

    Exemplo pre-definido para teste no Swagger:
    - user_id = 1

    Retorna os dados atualizados em caso de sucesso ou um erro 404 quando o
    usuario informado nao existe.
    """
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        return erro("usuario nao encontrado", 404)

    if payload.name is not None:
        user.name = payload.name
    if payload.email is not None:
        user.email = payload.email.lower()
    if payload.password is not None:
        user.password = payload.password
    if payload.is_active is not None:
        user.is_active = payload.is_active

    db.commit()
    db.refresh(user)
    return {
        "message": "Usuario atualizado com sucesso.",
        "data": user_to_dict(user),
    }


# DELETE /users/{user_id} -> remove um usuario pelo ID (404 se nao existir).
@router.delete(
    "/{user_id}",
    summary="Remove um usuario",
    description="Apaga do banco de dados o usuario correspondente ao `user_id` informado.",
)
def delete_user(
    user_id: int = Path(
        ...,
        examples=[1],
        description="ID do usuario que sera removido.",
    ),
    db: Session = Depends(get_db),
):
    """
    Remove um usuario cadastrado no banco de dados.

    Recebe o `user_id` pela URL e apaga o registro correspondente.

    Exemplo pre-definido para teste no Swagger:
    - user_id = 1

    Retorna o `id` do usuario removido em caso de sucesso ou um erro 404
    quando o usuario informado nao existe.
    """
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        return erro("usuario nao encontrado", 404)

    db.delete(user)
    db.commit()
    return {
        "status": "deleted",
        "id": user_id,
        "message": "Usuario removido com sucesso.",
    }
