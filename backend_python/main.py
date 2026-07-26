from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
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
    check_connection()
    seed_admin_user()
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
