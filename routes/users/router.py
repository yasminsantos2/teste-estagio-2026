from fastapi import APIRouter, Depends, Path, Query
from pydantic import BaseModel

from entities.user import User
from services.users import UserService, get_user_service


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


# Converte o modelo ORM em um dicionario serializavel para a resposta.
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


# POST /users/ -> cria um usuario apos validar nome, email, senha e duplicidade.
@router.post(
    "/",
    summary="Cria um novo usuario",
    description="Cadastra um novo usuario no banco de dados apos validar os dados enviados.",
)
def create_user(
    payload: UserCreate,
    service: UserService = Depends(get_user_service),
):
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
    user = service.create(payload.name, payload.email, payload.password)
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
    service: UserService = Depends(get_user_service),
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
    users = service.list(skip=skip, limit=limit)
    return {
        "message": "Lista de usuarios retornada com sucesso.",
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
    service: UserService = Depends(get_user_service),
):
    """
    Busca um unico usuario no banco de dados pelo seu ID.

    Recebe o `user_id` pela URL e retorna os dados do usuario correspondente.

    Exemplo pre-definido para teste no Swagger:
    - user_id = 1

    Retorna os dados do usuario em caso de sucesso ou um erro 404 quando o
    usuario informado nao existe.
    """
    user = service.get(user_id)
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
    service: UserService = Depends(get_user_service),
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
    user = service.update(
        user_id,
        name=payload.name,
        email=payload.email,
        password=payload.password,
        is_active=payload.is_active,
    )
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
    service: UserService = Depends(get_user_service),
):
    """
    Remove um usuario cadastrado no banco de dados.

    Recebe o `user_id` pela URL e apaga o registro correspondente.

    Exemplo pre-definido para teste no Swagger:
    - user_id = 1

    Retorna o `id` do usuario removido em caso de sucesso ou um erro 404
    quando o usuario informado nao existe.
    """
    service.delete(user_id)
    return {
        "status": "deleted",
        "id": user_id,
        "message": "Usuario removido com sucesso.",
    }
