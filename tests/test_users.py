def _payload(**overrides):
    base = {
        "name": "Maria Silva",
        "email": "maria.silva@email.com",
        "password": "senhaSegura123",
    }
    base.update(overrides)
    return base


class TestCreateUser:
    def test_create_user_success(self, client):
        response = client.post("/users/", json=_payload())

        assert response.status_code == 200
        body = response.json()
        assert body["message"] == "Usuario criado com sucesso."
        assert body["data"]["name"] == "Maria Silva"
        assert body["data"]["email"] == "maria.silva@email.com"
        assert body["data"]["id"] is not None

    def test_create_user_normaliza_email_minusculo(self, client):
        response = client.post("/users/", json=_payload(email="MARIA@EMAIL.COM"))

        assert response.status_code == 200
        assert response.json()["data"]["email"] == "maria@email.com"

    def test_create_user_nao_expoe_senha(self, client):
        response = client.post("/users/", json=_payload())

        assert response.status_code == 200
        assert "password" not in response.json()["data"]

    def test_create_user_nome_curto(self, client):
        response = client.post("/users/", json=_payload(name="ab"))

        assert response.status_code == 422
        assert response.json()["ok"] is False

    def test_create_user_email_invalido(self, client):
        response = client.post("/users/", json=_payload(email="semarroba"))

        assert response.status_code == 422
        assert response.json()["ok"] is False

    def test_create_user_senha_vazia(self, client):
        response = client.post("/users/", json=_payload(password=""))

        assert response.status_code == 422
        assert response.json()["ok"] is False

    def test_create_user_email_duplicado(self, client):
        client.post("/users/", json=_payload())

        response = client.post("/users/", json=_payload(name="Outro Nome"))

        assert response.status_code == 409
        assert response.json()["ok"] is False


class TestListUsers:
    def test_list_users_vazio(self, client):
        response = client.get("/users/")

        assert response.status_code == 200
        body = response.json()
        assert body["total"] == 0
        assert body["data"] == []

    def test_list_users_com_registros(self, client):
        client.post("/users/", json=_payload(email="a@email.com"))
        client.post("/users/", json=_payload(email="b@email.com"))

        response = client.get("/users/")

        assert response.status_code == 200
        assert response.json()["total"] == 2


class TestGetUser:
    def test_get_user_success(self, client):
        created = client.post("/users/", json=_payload()).json()["data"]

        response = client.get(f"/users/{created['id']}")

        assert response.status_code == 200
        assert response.json()["data"]["id"] == created["id"]

    def test_get_user_inexistente(self, client):
        response = client.get("/users/9999")

        assert response.status_code == 404
        assert response.json()["ok"] is False


class TestUpdateUser:
    def test_update_user_success(self, client):
        created = client.post("/users/", json=_payload()).json()["data"]

        response = client.patch(
            f"/users/{created['id']}", json={"name": "Maria Atualizada"}
        )

        assert response.status_code == 200
        assert response.json()["data"]["name"] == "Maria Atualizada"

    def test_update_user_desativar(self, client):
        created = client.post("/users/", json=_payload()).json()["data"]
        assert created["is_active"] is True

        response = client.patch(
            f"/users/{created['id']}", json={"is_active": False}
        )

        assert response.status_code == 200
        assert response.json()["data"]["is_active"] is False

    def test_update_user_inexistente(self, client):
        response = client.patch("/users/9999", json={"name": "Ninguem"})

        assert response.status_code == 404
        assert response.json()["ok"] is False


class TestDeleteUser:
    def test_delete_user_remove_o_correto(self, client):
        user_a = client.post("/users/", json=_payload(email="a@email.com")).json()["data"]
        user_b = client.post("/users/", json=_payload(email="b@email.com")).json()["data"]

        response = client.delete(f"/users/{user_a['id']}")

        assert response.status_code == 200
        assert response.json()["id"] == user_a["id"]
        # O usuario correto foi removido...
        assert client.get(f"/users/{user_a['id']}").status_code == 404
        # ...e o outro continua existindo.
        assert client.get(f"/users/{user_b['id']}").status_code == 200

    def test_delete_user_inexistente(self, client):
        response = client.delete("/users/9999")

        assert response.status_code == 404
        assert response.json()["ok"] is False
