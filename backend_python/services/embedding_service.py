from sentence_transformers import SentenceTransformer
import config
import logging
from typing import List

logger = logging.getLogger("embedding_service")

_model_instance = None

def get_embedding_model() -> SentenceTransformer:
    global _model_instance
    if _model_instance is None:
        model_name = config.EMBEDDING_MODEL_NAME
        logger.info(f"Carregando modelo SentenceTransformer: {model_name}...")
        _model_instance = SentenceTransformer(model_name)
        logger.info("Modelo SentenceTransformer carregado com sucesso!")
    return _model_instance

def generate_embedding(text: str) -> List[float]:
    """
    Gera um vetor embedding (lista de floats) para o texto fornecido com fallback seguro.
    """
    try:
        model = get_embedding_model()
        embedding = model.encode(text, convert_to_numpy=True).tolist()
        return embedding
    except Exception as e:
        logger.warning(f"Erro ao gerar embedding ({e}). Retornando vetor zerado de fallback.")
        return [0.0] * 384

def generate_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """
    Gera vetores embeddings em lote para otimizar velocidade com fallback seguro.
    """
    if not texts:
        return []
    try:
        model = get_embedding_model()
        embeddings = model.encode(texts, convert_to_numpy=True).tolist()
        return embeddings
    except Exception as e:
        logger.warning(f"Erro ao gerar embeddings em lote ({e}). Retornando vetores zerados.")
        return [[0.0] * 384 for _ in texts]

