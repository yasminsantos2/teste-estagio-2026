from datetime import datetime

from pydantic import BaseModel


# DTO de entrada para criacao de usuario (POST /users/).
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


# DTO de entrada para atualizacao parcial de usuario (PATCH /users/{id}).
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


# DTO de saida que representa um usuario (sem expor a senha).
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


# Envelope de resposta para operacoes com um unico usuario.
class UserMessageResponse(BaseModel):
    message: str
    data: UserResponse


# Envelope de resposta para a listagem de usuarios.
class UserListResponse(BaseModel):
    message: str
    total: int
    data: list[UserResponse]


# Envelope de resposta para a remocao de um usuario.
class UserDeleteResponse(BaseModel):
    status: str
    id: int
    message: str
