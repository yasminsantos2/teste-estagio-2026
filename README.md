# 🚀 Desafio Técnico - API de Usuários

## 📖 Contexto

Recentemente, um dos desenvolvedores da equipe recebeu a missão de criar uma API para gerenciamento de usuários.

O projeto foi entregue e já está funcionando, mas existe um detalhe: era a primeira vez que esse desenvolvedor trabalhava sozinho em uma API desse porte. 😅

Como acontece em muitos projetos reais, a aplicação evoluiu, algumas decisões foram tomadas com pressa, outras poderiam ter sido melhor planejadas e alguns pontos acabaram ficando para trás durante o desenvolvimento.

Agora você recebeu a responsabilidade de assumir essa base de código.

Sua missão não é reescrever tudo do zero.

Queremos entender como você investiga uma aplicação existente, identifica oportunidades de melhoria e realiza ajustes que deixem o projeto mais confiável, organizado e fácil de manter.

---

## 🎯 Objetivo

Analise a API existente e faça as melhorias que considerar necessárias.

Não existe uma lista fechada de problemas para corrigir.

Queremos observar como você explora a aplicação, interpreta o código e toma decisões técnicas para evoluir o projeto.

Pense como alguém que acabou de entrar em uma equipe e recebeu a tarefa de dar continuidade a um sistema já em produção.

---

## 🤖 Uso de Inteligência Artificial

O uso de ferramentas de IA é permitido.

No entanto, durante a avaliação, você poderá ser questionado sobre as alterações realizadas.

Por isso, é importante compreender e conseguir explicar as decisões tomadas ao longo do desenvolvimento.

---

## ▶️ Como Executar o Projeto

### Criar ambiente virtual

```bash
python -m venv .venv
```

### Ativar ambiente virtual

**Windows**

```bash
.venv\Scripts\activate
```

**Linux/MacOS**

```bash
source .venv/bin/activate
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Inicializar banco de dados

```bash
python database/seed.py
```

### Executar a API

```bash
uvicorn main:app --reload
```

### Documentação

```text
http://localhost:8000/api/users/docs
```

---

## 🧪 Testes

O projeto possui uma suíte de testes automatizados com **pytest** que cobre todos os endpoints de usuários.

### Configuração do ambiente de testes

Os testes rodam de forma isolada, sem afetar o banco de dados real (`dev.db`). Cada teste utiliza um banco **SQLite em memória** criado e destruído automaticamente, e a dependência `get_db` é sobrescrita para apontar para esse banco temporário.

Arquivos relacionados:

* `requirements-dev.txt` → dependências de desenvolvimento/teste (`pytest`, `httpx`);
* `pytest.ini` → configuração do pytest (descoberta de testes e opções);
* `tests/conftest.py` → fixtures que preparam o banco em memória e o cliente de teste;
* `tests/test_users.py` → testes dos endpoints de usuários.

### Instalar dependências de teste

```bash
pip install -r requirements-dev.txt
```

### Executar os testes

```bash
python -m pytest
```

Para ver a cobertura de cenários de um endpoint específico:

```bash
python -m pytest tests/test_users.py -k delete
```

---

## 📌 Endpoints Disponíveis

* `POST /users/`
* `GET /users/`
* `GET /users/{user_id}`
* `PATCH /users/{user_id}`
* `DELETE /users/{user_id}`

> **Nota:** o endpoint legado `POST /users/create` foi **removido** por ser redundante com `POST /users/` e por conter bugs (verificação de duplicidade incorreta e ausência de validações). Como o projeto não possui consumidores externos, optei pela remoção; em um cenário de produção, a rota seria marcada como `deprecated` antes de uma remoção definitiva.

---

## 🗂️ Modelo de Dados

Diagrama de classe da entidade `User` (tabela `users`):

```mermaid
classDiagram
    class User {
        +int id
        +str name
        +str email
        +str password
        +bool is_active
        +datetime created_at
        +datetime~None~ updated_at
    }
```

| Campo | Tipo | Restrições | Descrição |
|---|---|---|---|
| `id` | `int` | PK, indexado | Identificador único do usuário |
| `name` | `str(120)` | obrigatório | Nome do usuário |
| `email` | `str(255)` | obrigatório, indexado | E-mail do usuário |
| `password` | `str(255)` | obrigatório | Senha do usuário |
| `is_active` | `bool` | obrigatório, default `true` | Indica se o usuário está ativo |
| `created_at` | `datetime` | obrigatório, default `utc_now` | Data de criação do registro |
| `updated_at` | `datetime \| None` | opcional | Data da última atualização |

---

## 🧩 Diagrama de Casos de Uso

Representação dos casos de uso da API a partir do ator que a consome:

```mermaid
flowchart LR
    actor(("👤 Cliente da API"))

    subgraph API["API de Usuários"]
        uc1(["Criar usuário"])
        uc2(["Listar usuários"])
        uc3(["Buscar usuário por ID"])
        uc4(["Atualizar usuário"])
        uc5(["Remover usuário"])
    end

    actor --> uc1
    actor --> uc2
    actor --> uc3
    actor --> uc4
    actor --> uc5

    uc1 -. valida e persiste .-> DB[("Banco de Dados")]
    uc2 -. consulta .-> DB
    uc3 -. consulta .-> DB
    uc4 -. atualiza .-> DB
    uc5 -. remove .-> DB
```

| Caso de uso | Endpoint | Descrição |
|---|---|---|
| Criar usuário | `POST /users/` | Cadastra um novo usuário após validar os dados |
| Listar usuários | `GET /users/` | Lista os usuários com paginação (`skip`/`limit`) |
| Buscar usuário por ID | `GET /users/{user_id}` | Retorna um usuário específico |
| Atualizar usuário | `PATCH /users/{user_id}` | Atualiza parcialmente os dados de um usuário |
| Remover usuário | `DELETE /users/{user_id}` | Exclui um usuário do banco |

---

## 📦 O Que Esperamos na Entrega

Sua entrega deve conter:

* Código atualizado;
* Melhorias que você considerar relevantes;
* Instruções para execução do projeto;
* Explicação das alterações realizadas;
* Justificativas para decisões importantes;
---

## 📝 Importante

Não buscamos uma solução perfeita.

O objetivo deste desafio é entender como você trabalha com uma base de código existente, como investiga problemas, organiza suas ideias e evolui uma aplicação de forma incremental.

Explique suas decisões, documente seu raciocínio e sinta-se à vontade para apontar pontos que você optou por não alterar.

Boa sorte! 🍀
