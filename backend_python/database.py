from pymongo import MongoClient
import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("database")

if not config.MONGODB_URI:
    logger.warning("MONGODB_URI não encontrada nas variáveis de ambiente!")

client = MongoClient(config.MONGODB_URI)
try:
    db = client.get_database()
except Exception:
    db = client["iara"]


users_collection = db["users"]
chats_collection = db["chats"]
document_chunks_collection = db["document_chunks"]
code_examples_collection = db["code_examples"]

# Coleções para a nova pipeline RAG de 2 bases
exercise_catalog_collection = db["exercise_catalog"]
concept_base_collection = db["concept_base"]

def check_connection():
    try:
        client.admin.command('ping')
        logger.info("MongoDB Atlas: Conexão estabelecida com sucesso!")
        return True
    except Exception as e:
        logger.error(f"Erro ao conectar ao MongoDB Atlas: {e}")
        return False
