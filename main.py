from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
from database import create_database
from routes.users import router as users_router
from services.users import UserServiceError


# Cria as tabelas no banco durante a inicializacao da aplicacao.
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_database()
    yield


# Docs nativas desativadas; expostas em rota customizada abaixo.
app = FastAPI(
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
    openapi_url="/api/users/docs/openapi.json",
)


# Traduz erros de dominio do service para o formato de resposta padrao da API.
@app.exception_handler(UserServiceError)
async def handle_user_service_error(request: Request, exc: UserServiceError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "ok": False,
            "erro": exc.message,
            "status": exc.status_code,
            "comentario": "Nao foi possivel concluir a requisicao.",
        },
    )


# Swagger UI servido em um caminho proprio da API.
@app.get("/api/users/docs", include_in_schema=False)
async def custom_docs():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="Documentacao da API - CRUD Users",
    )


# Registra os endpoints de usuarios.
app.include_router(users_router)


# Permite rodar a API diretamente com `python main.py`.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
