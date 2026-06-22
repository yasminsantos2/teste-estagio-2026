import pytest

from services.users import (
    DuplicateEmailError,
    UserNotFoundError,
    UserService,
    UserValidationError,
)


@pytest.fixture()
def service(db_session):
    return UserService(db_session)


def _create_default(service, **overrides):
    data = {
        "name": "Maria Silva",
        "email": "maria.silva@email.com",
        "password": "senhaSegura123",
    }
    data.update(overrides)
    return service.create(**data)


class TestCreate:
    def test_create_success(self, service):
        user = _create_default(service)

        assert user.id is not None
        assert user.name == "Maria Silva"
        assert user.email == "maria.silva@email.com"
        assert user.is_active is True

    def test_create_normaliza_email_minusculo(self, service):
        user = _create_default(service, email="MARIA@EMAIL.COM")

        assert user.email == "maria@email.com"

    def test_create_nome_curto(self, service):
        with pytest.raises(UserValidationError):
            _create_default(service, name="ab")

    def test_create_email_invalido(self, service):
        with pytest.raises(UserValidationError):
            _create_default(service, email="semarroba")

    def test_create_senha_vazia(self, service):
        with pytest.raises(UserValidationError):
            _create_default(service, password="")

    def test_create_email_duplicado(self, service):
        _create_default(service)

        with pytest.raises(DuplicateEmailError):
            _create_default(service, name="Outro Nome")


class TestList:
    def test_list_vazio(self, service):
        assert service.list() == []

    def test_list_com_registros(self, service):
        _create_default(service, email="a@email.com")
        _create_default(service, email="b@email.com")

        assert len(service.list()) == 2


class TestGet:
    def test_get_success(self, service):
        created = _create_default(service)

        found = service.get(created.id)

        assert found.id == created.id

    def test_get_inexistente(self, service):
        with pytest.raises(UserNotFoundError):
            service.get(9999)


class TestUpdate:
    def test_update_success(self, service):
        created = _create_default(service)

        updated = service.update(created.id, name="Maria Atualizada")

        assert updated.name == "Maria Atualizada"

    def test_update_preenche_updated_at(self, service):
        created = _create_default(service)
        assert created.updated_at is None

        updated = service.update(created.id, name="Maria Atualizada")

        assert updated.updated_at is not None

    def test_update_desativar(self, service):
        created = _create_default(service)

        updated = service.update(created.id, is_active=False)

        assert updated.is_active is False

    def test_update_inexistente(self, service):
        with pytest.raises(UserNotFoundError):
            service.update(9999, name="Ninguem")


class TestDelete:
    def test_delete_success(self, service):
        created = _create_default(service)

        service.delete(created.id)

        with pytest.raises(UserNotFoundError):
            service.get(created.id)

    def test_delete_inexistente(self, service):
        with pytest.raises(UserNotFoundError):
            service.delete(9999)
