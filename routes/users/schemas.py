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
