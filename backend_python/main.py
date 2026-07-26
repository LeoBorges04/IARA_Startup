from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
import sys

# Garantir que o diretório backend_python esteja no sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uvicorn
import config
from database import check_connection
from services.auth_service import seed_admin_user
from routes.auth import router as auth_router
from routes.chats import router as chats_router
from routes.admin import router as admin_router
from routes.documents import router as documents_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando backend Python RAG da IARA...")
    if check_connection():
        try:
            seed_admin_user()
        except Exception as e:
            print(f"Aviso ao executar seed_admin_user: {e}")
    else:
        print("⚠️ Não foi possível conectar ao MongoDB Atlas. Verifique a MONGODB_URI no arquivo .env")
    yield

app = FastAPI(
    title="IARA - Tutor Inteligente com RAG",
    description="Backend em Python (FastAPI) com suporte a RAG (SentenceTransformers & MongoDB Atlas)",
    version="2.0.0",
    lifespan=lifespan
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas da API
app.include_router(auth_router)
app.include_router(chats_router)
app.include_router(admin_router)
app.include_router(documents_router)

# Serve o frontend estático na raiz
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=config.PORT, reload=True)
