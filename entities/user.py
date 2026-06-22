from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


# Retorna a data/hora atual em UTC (usada como default dos timestamps).
def utc_now() -> datetime:
    return datetime.now(timezone.utc)


# Modelo ORM que representa a tabela de usuarios no banco de dados.
class User(Base):
    __tablename__ = "users"

    # Identificador unico do usuario (chave primaria).
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # Nome do usuario.
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    # Email do usuario (indexado para buscas mais rapidas).
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    # Senha do usuario.
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    # Indica se o usuario esta ativo; novos usuarios ja nascem ativos.
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    # Data de criacao, preenchida automaticamente no cadastro.
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=utc_now)
    # Data da ultima atualizacao; nula enquanto nunca for editado.
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
