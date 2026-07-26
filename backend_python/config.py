import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env na pasta backend_python ou na raiz
env_path_python = os.path.join(os.path.dirname(__file__), ".env")
env_path_root = os.path.join(os.path.dirname(__file__), "..", ".env")

if os.path.exists(env_path_python):
    load_dotenv(env_path_python)
elif os.path.exists(env_path_root):
    load_dotenv(env_path_root)
else:
    load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "")
PORT = int(os.getenv("PORT", 3000))
API_KEY = os.getenv("API_KEY", "")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
