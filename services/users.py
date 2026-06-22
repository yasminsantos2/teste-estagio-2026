from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db
from entities.user import User
from repository import users as users_repo


# Erro base do dominio de usuarios; o status_code orienta a resposta HTTP.
class UserServiceError(Exception):
    status_code = 500

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


# Dados de entrada invalidos.
class UserValidationError(UserServiceError):
    status_code = 422


# Email ja cadastrado por outro usuario.
class DuplicateEmailError(UserServiceError):
    status_code = 409


# Usuario inexistente.
class UserNotFoundError(UserServiceError):
    status_code = 404


# Concentra as regras de negocio de usuarios, isolando o router do repositorio.
class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, email: str, password: str) -> User:
        if len(name) < 3:
            raise UserValidationError("nome muito curto; informe ao menos 3 caracteres")
        if "@" not in email:
            raise UserValidationError("email invalido; o caractere @ esta faltando")
        if password == "":
            raise UserValidationError("senha obrigatoria; informe uma senha valida")

        if users_repo.get_user_by_email(self.db, email.strip().lower()):
            raise DuplicateEmailError("ja existe um usuario cadastrado com esse email")

        try:
            return users_repo.create_user(
                self.db, name=name, email=email, password=password
            )
        except IntegrityError:
            self.db.rollback()
            raise UserServiceError("nao foi possivel salvar o usuario no banco de dados")

    def list(self, skip: int = 0, limit: int = 100) -> list[User]:
        return users_repo.list_users(self.db, skip=skip, limit=limit)

    def get(self, user_id: int) -> User:
        user = users_repo.get_user(self.db, user_id)
        if user is None:
            raise UserNotFoundError("usuario nao encontrado")
        return user

    def update(
        self,
        user_id: int,
        *,
        name: str | None = None,
        email: str | None = None,
        password: str | None = None,
        is_active: bool | None = None,
    ) -> User:
        user = self.get(user_id)
        return users_repo.update_user(
            self.db,
            user,
            name=name,
            email=email,
            password=password,
            is_active=is_active,
        )

    def delete(self, user_id: int) -> None:
        user = self.get(user_id)
        users_repo.delete_user(self.db, user)


# Provedor de dependencia: injeta o UserService com a sessao do banco.
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)
