# Desafio Tecnico - CRUD de Usuarios

## Contexto

Voce recebeu uma API ja iniciada para gerenciamento de usuarios. A aplicacao usa FastAPI, SQLAlchemy e SQLite, mas ainda precisa de manutencao para ficar mais confiavel, organizada e facil de evoluir.

O objetivo deste desafio nao e criar um CRUD do zero. O foco e analisar uma base existente, entender como ela funciona, identificar problemas, corrigir comportamentos incorretos e melhorar a qualidade do codigo sem reescrever tudo sem necessidade.

O uso de inteligencia artificial e permitido. Ainda assim, voce devera ser capaz de explicar todas as alteracoes realizadas, justificar suas decisoes tecnicas e demonstrar entendimento real sobre o codigo entregue.

## O Que Deve Ser Feito

Analise o projeto e faca melhorias que voce considerar importantes para tornar a API mais correta e manutenivel.

Pontos que esperamos que voce observe:

- bugs de logica;
- validacoes incompletas ou inconsistentes;
- tratamento inadequado de erros;
- responsabilidades mal distribuidas entre rotas, repositorios, entidades e funcoes;
- padronizacao de respostas e mensagens;
- organizacao geral do projeto;
- ausencia de testes importantes;
- comportamentos que podem quebrar em cenarios simples de uso.

Voce nao precisa implementar funcionalidades grandes fora do escopo de usuarios. Prefira melhorias pequenas, bem justificadas e que deixem o projeto mais facil de manter.

## Como Rodar

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

Instale as dependencias:

```bash
pip install -r requirements.txt
```

Inicialize o banco SQLite:

```bash
python database/seed.py
```

Rode a API:

```bash
uvicorn main:app --reload
```

A documentacao fica disponivel em:

```text
http://localhost:8000/api/users/docs
```

## Endpoints Existentes

- `POST /users/`
- `GET /users/`
- `GET /users/{user_id}`
- `PATCH /users/{user_id}`
- `DELETE /users/{user_id}`

## Regras Gerais

- Mantenha a estrutura atual do projeto como base.
- Evite reescrever a aplicacao inteira.
- Explique no seu README ou em um arquivo separado o que voce encontrou e o que alterou.
- Se criar testes, explique como executa-los.
- Se decidir nao corrigir algum ponto, explique o motivo.
- Se usar IA, revise o resultado e esteja preparado para defender as decisoes.

## Entrega Esperada

Sua entrega deve conter:

- codigo corrigido e organizado;
- instrucoes claras para rodar o projeto;
- descricao objetiva das principais alteracoes feitas;
- justificativas tecnicas para as mudancas mais relevantes;
- testes automatizados, quando possivel.

## O Que Sera Avaliado

Vamos avaliar principalmente:

- capacidade de ler e entender codigo existente;
- atencao aos detalhes;
- raciocinio para encontrar bugs e inconsistencias;
- clareza nas correcoes;
- organizacao do codigo;
- cuidado com validacoes e erros;
- nocao basica de testes;
- capacidade de explicar as proprias decisoes.

Para vaga de estagio, nao esperamos uma solucao perfeita. Queremos ver como voce pensa, como investiga problemas e como melhora uma base de codigo realista aos poucos.
