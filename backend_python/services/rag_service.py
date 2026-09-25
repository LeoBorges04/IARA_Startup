import logging
import re
import numpy as np
from typing import List, Dict, Any, Optional
import os
import pypdf
from database import document_chunks_collection
from services.embedding_service import generate_embedding, generate_embeddings_batch
from langchain_text_splitters import RecursiveCharacterTextSplitter
import config
from openai import OpenAI

logger = logging.getLogger("rag_service")

# Instância/helper para o cliente OpenAI com suporte a lazy loading
_openai_client: Optional[OpenAI] = None

def get_openai_client() -> Optional[OpenAI]:
    global _openai_client
    if _openai_client is None and config.API_KEY:
        try:
            _openai_client = OpenAI(api_key=config.API_KEY)
        except Exception as e:
            logger.error(f"Erro ao inicializar cliente OpenAI: {e}")
            return None
    return _openai_client

def chunk_text(text: str, chunk_size: int = 600, chunk_overlap: int = 100) -> List[str]:
    """
    Fatia o texto em blocos de tamanho controlado com sobreposição.
    """
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        return splitter.split_text(text)
    except Exception as e:
        logger.error(f"Erro ao fatiar texto: {e}")
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += (chunk_size - chunk_overlap)
        return chunks

def extract_text_from_file(file_path: str, filename: str) -> str:
    """
    Extrai o conteúdo de texto de arquivos TXT, PDF, MD, C++, PY, etc.
    """
    ext = os.path.splitext(filename)[1].lower()
    
    if ext == ".pdf":
        text_content = ""
        reader = pypdf.PdfReader(file_path)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text_content += extracted + "\n"
        return text_content
    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

def extract_chunks_with_metadata(file_path: str, filename: str, chunk_size: int = 600, chunk_overlap: int = 100) -> List[Dict[str, Any]]:
    """
    Extrai o texto de um arquivo (PDF, TXT, MD, C++, PY) preservando metadados de página e/ou seção.
    """
    ext = os.path.splitext(filename)[1].lower()
    chunks_with_meta = []
    
    if ext == ".pdf":
        try:
            reader = pypdf.PdfReader(file_path)
            for page_idx, page in enumerate(reader.pages, start=1):
                extracted = page.extract_text()
                if extracted and extracted.strip():
                    page_chunks = chunk_text(extracted, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                    for c_str in page_chunks:
                        chunks_with_meta.append({
                            "content": c_str,
                            "page_number": page_idx,
                            "location": f"Página {page_idx}"
                        })
        except Exception as e:
            logger.error(f"Erro ao extrair PDF por páginas '{filename}': {e}")
    else:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                raw_text = f.read()
            
            raw_chunks = chunk_text(raw_text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            for idx, c_str in enumerate(raw_chunks, start=1):
                first_line = c_str.strip().split("\n")[0] if c_str.strip() else ""
                section_name = ""
                if first_line.startswith("#"):
                    section_name = f" (Seção: '{first_line.lstrip('#').strip()}')"
                
                chunks_with_meta.append({
                    "content": c_str,
                    "page_number": None,
                    "location": f"Trecho {idx}{section_name}"
                })
        except Exception as e:
            logger.error(f"Erro ao ler arquivo '{filename}': {e}")

    return chunks_with_meta

CHUNK_STRUCTURE_PROMPT = """Você receberá um material didático sobre programação. Sua tarefa é dividir esse material em pequenos chunks independentes, otimizados para indexação em um sistema RAG (Retrieval-Augmented Generation).

Não resuma o conteúdo, não invente informações e não remova detalhes importantes. Apenas reorganize o material em blocos menores e semanticamente completos.

### Regras
* Cada chunk deve abordar apenas um único conceito.
* Nunca misture assuntos diferentes no mesmo chunk.
* Cada chunk deve ser compreensível mesmo que seja lido isoladamente.
* Preserve exemplos de código, mas mantenha apenas aqueles relacionados ao assunto do chunk.
* Se uma seção abordar mais de um conceito (por exemplo, while, do while e for), divida-a em chunks separados.
* Não crie exercícios resolvidos.
* Não modifique a sintaxe dos exemplos.
* Não altere a linguagem de programação.
* Não adicione conteúdo que não esteja presente no material original.

### Estrutura de cada chunk
Cada chunk deve seguir exatamente este formato:

Linguagem:
Categoria:
Subcategoria:
Título:

Descrição:

Código:

Observações:

---
(Use '---' em uma nova linha separada para delimitar cada chunk)
"""

def semantic_chunk_text_with_llm(text_content: str, filename: str) -> List[Dict[str, Any]]:
    """
    Utiliza o modelo OpenAI (gpt-4o-mini) para reestruturar e dividir o material didático 
    em chunks independentes e padronizados no formato estrito solicitado.
    """
    client = get_openai_client()
    if not client or len(text_content.strip()) < 40:
        return []

    logger.info(f"Executando Fatiamento Semântico Estruturado (LLM Chunking) para '{filename}'...")
    
    text_blocks = []
    max_llm_input = 4000
    start = 0
    while start < len(text_content):
        end = min(start + max_llm_input, len(text_content))
        if end < len(text_content):
            last_newline = text_content.rfind("\n\n", start, end)
            if last_newline > start:
                end = last_newline
        text_blocks.append(text_content[start:end])
        start = end

    all_structured_chunks = []
    for b_idx, block in enumerate(text_blocks):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": CHUNK_STRUCTURE_PROMPT},
                    {"role": "user", "content": f"Material didático (Parte {b_idx + 1}):\n\n{block}"}
                ],
                temperature=0.1,
                max_tokens=1500
            )
            raw_response = response.choices[0].message.content.strip()
            
            chunks_raw = raw_response.split("---")
            for c_raw in chunks_raw:
                c_clean = c_raw.strip()
                if c_clean and len(c_clean) > 30 and ("Linguagem:" in c_clean or "Descrição:" in c_clean or "Título:" in c_clean):
                    title_match = re.search(r"Título:\s*(.*)", c_clean)
                    title_str = title_match.group(1).strip() if title_match else f"Conceito {len(all_structured_chunks)+1}"
                    
                    all_structured_chunks.append({
                        "content": c_clean,
                        "page_number": None,
                        "location": f"Chunk Semântico: {title_str}"
                    })
        except Exception as e:
            logger.error(f"Erro no Fatiamento Semântico LLM para bloco {b_idx+1} de '{filename}': {e}")

    return all_structured_chunks

# Mapeamento das Coleções Vetoriais no MongoDB Atlas
from database import exercise_catalog_collection, concept_base_collection, classes_collection, document_chunks_collection

def chunk_markdown_by_h2(text_content: str) -> List[Dict[str, Any]]:
    """
    Fatia o material didático estritamente pelos cabeçalhos '## '.
    Cada bloco demarcado por '## ' gera exatamente um documento vetorial independente.
    Sem tamanho fixo por caracteres, sem overlap.
    """
    partes = re.split(r"^##\s+", text_content, flags=re.MULTILINE)
    chunks_meta = []
    
    for idx, parte in enumerate(partes):
        if not parte.strip():
            continue
            
        linhas = parte.split("\n", 1)
        titulo = linhas[0].strip()
        conteudo = linhas[1].strip() if len(linhas) > 1 else ""
        
        full_chunk_text = f"## {titulo}\n\n{conteudo}" if conteudo else f"## {titulo}"
        
        chunks_meta.append({
            "title": titulo,
            "content": full_chunk_text,
            "page_number": None,
            "location": f"Seção: {titulo}"
        })
        
    return chunks_meta

def extract_concepts_from_exercise_text(text: str) -> List[str]:
    """Extrai os itens listados sob a seção 'Conceitos envolvidos' do documento do exercício."""
    concepts = []
    match = re.search(r"Conceitos envolvidos:?\s*\n([\s\S]*?)(?=\n\s*(?:Palavras-chave|Pode aparecer como|Categoria|Dificuldade|##)|$)", text, re.IGNORECASE)
    if match:
        block = match.group(1)
        lines = block.split("\n")
        for line in lines:
            cleaned = re.sub(r"^[\s\-\*]+", "", line).strip()
            if cleaned:
                concepts.append(cleaned)
    return concepts

def update_class_rag_summary(class_id: str) -> str:
    """
    Identifica os assuntos e materiais contidos no acervo RAG da turma.
    Gera um resumo estruturado dos tópicos cobertos e armazena no documento da turma no MongoDB.
    """
    if not class_id:
        return ""

    try:
        from bson import ObjectId
        obj_id = ObjectId(class_id)
    except Exception:
        return ""

    filter_query = {"class_id": class_id}

    chunks = list(document_chunks_collection.find(filter_query, {"filename": 1, "title": 1, "location": 1}))
    concepts = list(concept_base_collection.find(filter_query, {"filename": 1, "title": 1, "location": 1}))
    exercises = list(exercise_catalog_collection.find(filter_query, {"filename": 1, "title": 1, "concepts_involved": 1}))

    filenames = set()
    topic_titles = set()
    concepts_list = set()

    for c in chunks + concepts:
        if c.get("filename"):
            filenames.add(c.get("filename"))
        t = c.get("location") or c.get("title")
        if t and len(t) > 3 and not str(t).startswith("Chunk Semântico"):
            topic_titles.add(str(t).strip())

    for e in exercises:
        if e.get("filename"):
            filenames.add(e.get("filename"))
        for conc in e.get("concepts_involved", []):
            if conc and len(str(conc)) > 2:
                concepts_list.add(str(conc).strip())

    if not filenames and not topic_titles and not concepts_list:
        rag_summary = "Nenhum documento cadastrado no acervo RAG desta turma até o momento."
    else:
        files_str = ", ".join(f"'{f}'" for f in sorted(list(filenames)))
        topics_str = ", ".join(sorted(list(topic_titles))[:15])
        conc_str = ", ".join(sorted(list(concepts_list))[:15])

        summary_parts = []
        if files_str:
            summary_parts.append(f"Materiais no acervo RAG: {files_str}")
        if topics_str:
            summary_parts.append(f"Tópicos e Seções cobertas: {topics_str}")
        if conc_str:
            summary_parts.append(f"Conceitos e Exercícios acervados: {conc_str}")

        rag_summary = "\n".join(summary_parts)

    try:
        from datetime import datetime
        classes_collection.update_one(
            {"_id": obj_id},
            {"$set": {
                "rag_summary": rag_summary,
                "rag_summary_updated_at": datetime.utcnow()
            }}
        )
    except Exception as e:
        logger.error(f"Erro ao salvar rag_summary da turma {class_id}: {e}")

    return rag_summary

def ingest_exercise_catalog(filename: str, content: Optional[str] = None, file_path: Optional[str] = None, class_id: Optional[str] = None) -> int:
    """
    Ingere documentos no Catálogo de Exercícios (Base 1).
    NUNCA contém códigos ou soluções. Índice semântico exclusivo por '## '.
    """
    if file_path and os.path.exists(file_path):
        raw_text = extract_text_from_file(file_path, filename)
    elif content:
        raw_text = content
    else:
        return 0

    if not raw_text or not raw_text.strip():
        return 0

    chunks_meta = chunk_markdown_by_h2(raw_text)
    if not chunks_meta:
        chunks_meta = [{"title": filename, "content": raw_text, "location": filename}]

    chunks_text = [c["content"] for c in chunks_meta]
    logger.info(f"Base 1 (Exercícios): Gerando embeddings para {len(chunks_text)} documentos de '{filename}' (Turma: {class_id})...")
    embeddings = generate_embeddings_batch(chunks_text)

    docs_to_insert = []
    for idx, (c_meta, emb) in enumerate(zip(chunks_meta, embeddings)):
        concepts = extract_concepts_from_exercise_text(c_meta["content"])
        docs_to_insert.append({
            "filename": filename,
            "chunk_index": idx,
            "title": c_meta.get("title", filename),
            "location": c_meta.get("location", filename),
            "content": c_meta["content"],
            "concepts_involved": concepts,
            "embedding": emb,
            "category": "exercise",
            "class_id": class_id
        })

    if docs_to_insert:
        del_filter = {"filename": filename}
        if class_id:
            del_filter["class_id"] = class_id
        exercise_catalog_collection.delete_many(del_filter)
        result = exercise_catalog_collection.insert_many(docs_to_insert)
        if class_id:
            update_class_rag_summary(class_id)
        return len(result.inserted_ids)
    return 0

def ingest_concept_base(filename: str, content: Optional[str] = None, file_path: Optional[str] = None, category: str = "concept", class_id: Optional[str] = None) -> int:
    """
    Ingere documentos na Base Conceitual (Base 2).
    Contém a explicação teórica e os esqueletos genéricos por '## '.
    """
    if file_path and os.path.exists(file_path):
        raw_text = extract_text_from_file(file_path, filename)
    elif content:
        raw_text = content
    else:
        return 0

    if not raw_text or not raw_text.strip():
        return 0

    chunks_meta = chunk_markdown_by_h2(raw_text)
    if not chunks_meta:
        chunks_meta = [{"title": filename, "content": raw_text, "location": filename}]

    chunks_text = [c["content"] for c in chunks_meta]
    logger.info(f"Base 2 (Conceitual): Gerando embeddings para {len(chunks_text)} documentos de '{filename}' (Turma: {class_id})...")
    embeddings = generate_embeddings_batch(chunks_text)

    docs_to_insert = []
    for idx, (c_meta, emb) in enumerate(zip(chunks_meta, embeddings)):
        docs_to_insert.append({
            "filename": filename,
            "chunk_index": idx,
            "title": c_meta.get("title", filename),
            "location": c_meta.get("location", filename),
            "content": c_meta["content"],
            "embedding": emb,
            "category": category,
            "class_id": class_id
        })

    if docs_to_insert:
        del_filter = {"filename": filename}
        if class_id:
            del_filter["class_id"] = class_id
        concept_base_collection.delete_many(del_filter)
        document_chunks_collection.delete_many(del_filter)
        
        concept_base_collection.insert_many(docs_to_insert)
        result = document_chunks_collection.insert_many(docs_to_insert)
        if class_id:
            update_class_rag_summary(class_id)
        return len(result.inserted_ids)
    return 0

def ingest_document(filename: str, content: Optional[str] = None, file_path: Optional[str] = None, category: str = "concept", class_id: Optional[str] = None) -> int:
    """Roteador principal de ingestão com suporte a class_id."""
    if category == "exercise":
        res = ingest_exercise_catalog(filename, content=content, file_path=file_path, class_id=class_id)
    else:
        res = ingest_concept_base(filename, content=content, file_path=file_path, category=category, class_id=class_id)
    if class_id:
        update_class_rag_summary(class_id)
    return res

def cosine_similarity(a: List[float], b: List[float]) -> float:
    vec_a = np.array(a, dtype=np.float32)
    vec_b = np.array(b, dtype=np.float32)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(vec_a, vec_b) / (norm_a * norm_b))

def search_exercise_catalog(query: str, class_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Busca o exercício correspondente na Base 1 (Catálogo de Exercícios) com filtro de turma."""
    query_vector = generate_embedding(query)
    filter_query = {}
    if class_id:
        filter_query["class_id"] = class_id

    all_docs = list(exercise_catalog_collection.find(filter_query, {"filename": 1, "title": 1, "content": 1, "concepts_involved": 1, "embedding": 1, "class_id": 1}))
    if not all_docs:
        return None

    best_score = -1.0
    best_doc = None
    for doc in all_docs:
        emb = doc.get("embedding")
        if emb:
            score = cosine_similarity(query_vector, emb)
            if score > best_score:
                best_score = score
                best_doc = doc

    return best_doc if (best_doc and best_score > 0.45) else None

def search_concept_base(query: str, top_k: int = 3, category: Optional[str] = None, class_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Busca tópicos conceituais e livros acervados na Base 2 e no acervo de documentos filtrando por turma."""
    query_vector = generate_embedding(query)
    filter_query = {}
    if category:
        filter_query["category"] = category
    if class_id:
        filter_query["class_id"] = class_id

    docs_concept = list(concept_base_collection.find(filter_query))
    docs_books = list(document_chunks_collection.find(filter_query))

    all_docs = docs_concept + docs_books
    if not all_docs:
        return []

    scored_docs = []
    query_words = set(re.findall(r'\w+', query.lower()))
    for doc in all_docs:
        emb = doc.get("embedding")
        score = 0.0
        if emb and any(v != 0 for v in emb[:5]):
            try:
                score = cosine_similarity(query_vector, emb)
            except Exception:
                score = 0.0
        
        if score <= 0.3:
            doc_text = (str(doc.get("title", "")) + " " + str(doc.get("content", "")) + " " + str(doc.get("filename", ""))).lower()
            matches = sum(1 for w in query_words if len(w) > 2 and w in doc_text)
            if matches > 0:
                score = max(score, 0.4 + (matches * 0.1))

        if score > 0.35:
            scored_docs.append((score, doc))

    scored_docs.sort(key=lambda x: x[0], reverse=True)
    return [doc for score, doc in scored_docs[:top_k]]


def search_relevant_chunks(query: str, top_k: int = 4, category: Optional[str] = None, class_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Wrapper para compatibilidade."""
    return search_concept_base(query, top_k=top_k, category=category, class_id=class_id)

def detect_user_intent(user_message: str) -> str:
    """
    Detecta a intenção principal da mensagem do usuário:
    - 'GREETING': saudações e conversas informais.
    - 'CONCEPTUAL_QUESTION': dúvidas teóricas/práticas de programação ("como fazer", "o que é", "como uso", "como fzr", "vetor", etc.).
    - 'EXERCISE': criação ou resolução de exercícios.
    - 'GENERAL_QUERY': outras perguntas.
    """
    msg_lower = user_message.lower().strip()

    # 1. Saudações
    greeting_terms = ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite", "tudo bem", "tudo bom", "fala iara", "e aí", "e ai", "quem é você", "quem e voce"]
    if any(msg_lower.startswith(g) or msg_lower == g for g in greeting_terms) and len(msg_lower.split()) <= 6:
        if not any(k in msg_lower for k in ["c++", "codigo", "código", "vetor", "vetors", "matriz", "função", "funcao", "loop", "for", "while", "algoritmo", "algoritimo", "fzr"]):
            return "GREETING"

    # 2. Dúvidas ou solicitações conceituais/práticas sobre programação
    prog_keywords = [
        "por que", "porque", "qual a diferença", "qual é a diferença", 
        "o que é", "o que faz", "como funciona", "para que serve",
        "dúvida", "duvida", "não entendi", "nao entendi", "explique",
        "como uso", "como usar", "qual o papel", "qual e o papel", "significa",
        "como fzr", "como fazer", "como declarar", "como criar", "como implementar",
        "vetor", "vetors", "matriz", "matrizes", "laço", "laco", "for", "while", "c++", "ponteiro", "struct"
    ]
    is_prog_query = any(k in msg_lower for k in prog_keywords)
    has_exercise_prompt = any(k in msg_lower for k in ["faça um programa para", "crie um algoritmo para", "escreva um código para", "como fazer um programa para", "exercício de", "exercicio de", "desafio de"])

    if is_prog_query and not has_exercise_prompt:
        return "CONCEPTUAL_QUESTION"
    
    if has_exercise_prompt:
        return "EXERCISE"

    return "GENERAL_QUERY"

def has_student_code(text: str) -> bool:
    """Verifica se a mensagem do usuário contém uma tentativa de código."""
    if "```" in text:
        return True
    code_tokens = ["#include", "cin", "cout", "for(", "for (", "while(", "while (", "if(", "if (", "int ", "float ", "double ", "void ", "return ", "struct ", "printf", "scanf", ";"]
    matches = sum(1 for t in code_tokens if t in text.lower())
    return matches >= 2

def strip_code_blocks(text: str) -> str:
    """Remove blocos de código Markdown de respostas de correção para manter feedback 100% conceitual."""
    return re.sub(r"```[\s\S]*?```", "", text).strip()

FEW_SHOT_PBL_EXAMPLES = """
=== EXEMPLOS DEMONSTRATIVOS DE COMPORTAMENTO DA TUTORA IARA (FEW-SHOT EXEMPLARS) ===

[EXEMPLO 1 - ABERTURA DO DESAFIO: PEDINDO A ETAPA 1 COM SIMPLICIDADE DIDÁTICA E CÓDIGO GENÉRICO]
Aluno: "Quero aprender como ler 5 notas em um vetor e encontrar a maior nota em C++"
IARA:
Desafio: Ler 5 notas em um vetor e encontrar a maior nota digitada.

---
### 📢 Etapa 1: Entrada de Dados e Boas Práticas

**Justificativa da Escolha Conceitual:**
1. **Uso de `#define TAM 5`**: O tamanho do vetor é fixo e conhecido antes da execução. A constante no topo evita números mágicos.
2. **Vetor `float`**: Notas possuem casas decimais.
3. **Laço `for` Exclusivo de Entrada**: Este laço é dedicado exclusivamente para a leitura dos dados, sem misturar nenhuma outra lógica.

**Onde Implementar no Código:**
- A diretiva `#define TAM 5` deve ficar no topo do arquivo (fora da main).
- A declaração do vetor e o laço exclusivo de leitura devem ser colocados no início da função `main()`.

**Código Genérico (Template Sintático 100% Abstrato e Simples):**
```cpp
// 1. Diretivas no topo (fora do main)
#define NOME_CONSTANTE VALOR

// 2. Início do main
int main() {
    tipo nomeVetor[NOME_CONSTANTE];
    
    // 3. Laço exclusivo de leitura (Responsabilidade Única)
    for (int i = 0; i < NOME_CONSTANTE; i++) {
        cin >> nomeVetor[i];
    }
    return 0;
}
```

**Instrução:**
Escreva o código da Etapa 1 com o `#define TAM 5` no topo e o laço dedicado de leitura no início da função `main()`.

[EXEMPLO 2 - PROCESSAMENTO COM ESTRUTURAS ATÔMICAS SIMPLES (DIDÁTICA ACIMA DA PERFORMANCE)]
Aluno:
```cpp
#include <iostream>
using namespace std;
#define TAM 5

int main() {
    float medias[TAM];
    for (int i = 0; i < TAM; i++) {
        cin >> medias[i];
    }
    return 0;
}
```
IARA:
Etapa 1 aprovada!

---
### 📢 Etapa 2: Processamento de Dados (Estruturas Simples por Regra de Negócio)

**Princípio Didático (Simplicidade e Clareza Lógica):**
Priorizamos a didática e a simplicidade sobre a performance do código. Cada regra de negócio do exercício é isolada em sua própria estrutura simples para facilitarmos a compreensão:

1. **Estrutura 1 (Busca do Maior)**: Um laço simples dedicado exclusivamente para encontrar o maior valor.
2. **Estrutura 2 (Busca do Menor)**: Um segundo laço simples separado exclusivamente para encontrar o menor valor.
3. **Estrutura 3 (Contagem de Aprovação)**: Um terceiro laço simples dedicado para classificar e contar aprovados/reprovados.

**Explicação Lógica (Sem Código):**
- Laço 1: Inicialize `maior = medias[0]` e compare elemento por elemento.
- Laço 2: Inicialize `menor = medias[0]` e compare elemento por elemento em um laço separado.
- Laço 3: Percorra o vetor e teste a condição de aprovação ($\ge 7$) incrementando o contador.

**Código Genérico (Template de Sintaxe 100% Abstrato e Desacoplado):**
```cpp
// --- ESTRUTURA 1: Busca do Maior (Laço Exclusivo 1) ---
tipoVar variavelMaior = nomeVetor[0];
for (int i = 1; i < NOME_CONSTANTE; i++) {
    if (sua_condicao_maior) {
        variavelMaior = nomeVetor[i];
    }
}

// --- ESTRUTURA 2: Busca do Menor (Laço Exclusivo 2) ---
tipoVar variavelMenor = nomeVetor[0];
for (int i = 1; i < NOME_CONSTANTE; i++) {
    if (sua_condicao_menor) {
        variavelMenor = nomeVetor[i];
    }
}

// --- ESTRUTURA 3: Contagem e Classificação (Laço Exclusivo 3) ---
int contadorAprovados = 0;
for (int i = 0; i < NOME_CONSTANTE; i++) {
    if (sua_condicao_aprovado) {
        contadorAprovados++;
    }
}
```

**Instrução:**
Pegue o seu código da Etapa 1 e inclua nele o processamento da Etapa 2, separando a busca do maior, a busca do menor e a contagem de aprovados em laços `for` simples e independentes.
"""

SYSTEM_PROMPT = f"""Você é IARA, uma tutora virtual baseada em Aprendizagem Baseada em Problemas (PBL Interativo) para matérias de computação e algoritmos.
Sua comunicação é ESTRITAMENTE OBJETIVA, DIRETA E CONCISA. É PROIBIDO o uso de frases motivacionais prolixas, saudações longas ou emojis.

=== DIRETRIZES DE ESCOPO, EMPATIA E RESTRIÇÃO DE CONTEÚDO (USO DA BASE DE DADOS RAG) ===
1. COMPREENSÃO E INTERPRETAÇÃO FLEXÍVEL DAS ENTRADAS:
   - A IARA deve compreender e interpretar qualquer entrada do usuário independentemente do assunto, linguagem informal ou erros de digitação (ex: "fzr", "vetors", "algoritimo", "laço for", etc.).
   - Para saudações simples ou apresentações (ex: "Oi", "Tudo bem?", "Quem é você?"), responda de forma cortês, amigável e breve, apresentando-se como IARA, a tutora virtual da turma.

2. TRATAMENTO DE ERROS DE DIGITAÇÃO E LINGUAGEM INFORMAL EM PROGRAMAÇÃO:
   - Interprete a intenção real de programação do aluno mesmo se houver erros ortográficos, abreviações ou digitação informal.
   - Se a intenção corresponder a conceitos cobertos no acervo RAG (ex: vetores, laços, condicionais, funções, C++, etc.), ensine e guie o aluno normalmente.

3. MANEJO EMPÁTICO DE ASSUNTOS FORA DA BASE DE CONHECIMENTO (FORA DO RAG / OFF-TOPIC):
   - A IARA DEVE ensinar APENAS os assuntos e matérias que estejam presentes e cobertos em sua base de dados RAG da turma (livros, apostilas, conceitos e exercícios disponibilizados pelo professor).
   - Quando o aluno perguntar ou mencionar assuntos que NÃO ESTÃO COBERTOS no acervo RAG (por exemplo: "Flamengo", futebol, receitas, política, celebridades, outras matérias não cadastradas ou conversa aleatória):
     * A IARA NÃO DEVE engajar na explicação nem responder/pesquisar sobre o assunto externo.
     * A IARA DEVE responder de forma amigável, acolhedora, educada e natural (JAMAIS dura, fria, robótica ou repetição mecânica de frases prontas).
     * Reconheça brevemente o que o aluno disse, explique com clareza e empatia que seu papel como tutora virtual nesta turma é dedicado exclusivamente aos conteúdos disponibilizados pelo professor no acervo, e convide-o gentilmente a trazer suas dúvidas ou estudos sobre a matéria da turma.

4. USO DA IA PARA COMPLEMENTAR ASSUNTOS JÁ COBERTOS:
   - Se o assunto solicitado ESTIVER presente nos documentos do acervo RAG, a IARA ensina o tópico embasando-se no acervo.
   - Quando necessário, a IARA pode utilizar a inteligência artificial para gerar uma resposta mais rica e bem fundamentada EXPANDINDO SOBRE O TÓPICO QUE O DOCUMENTO JÁ COBRE.

=== REGRAS DE INTERAÇÃO (MODO PBL PASSO A PASSO CUMULATIVO) ===
1. PRINCIPIO DA SIMPLICIDADE DIDÁTICA MÁXIMA (DIDÁTICA ACIMA DA PERFORMANCE):
   - O código DEVE ser o mais didático, simples e legível possível. JAMAIS busque otimização de performance, reuso excessivo de laços ou condensação de código.
   - CADA REGRA DE NEGÓCIO OU CONCEITO DISTINTO DO EXERCÍCIO DEVE TER SUA PRÓPRIA ESTRUTURA SINTÁTICA SIMPLES E INDEPENDENTE.
   - NUNCA junte em um mesmo laço `for` ou condicional regras de negócio que não são conceitualmente idênticas.
   - Exemplo: A busca do maior valor usa um `for` simples com `if`. A busca do menor valor usa OUTRO `for` simples com `if` separado. A contagem de aprovados usa OUTRO `for` separado.
   - Evite laços com muitas tarefas ou condicionais muito complexas que dificultem o aprendizado do aluno.

2. REGRA DE ABSTRAÇÃO 100% PURA NOS TEMPLATES GENÉRICOS:
   - O Código Genérico (Template de Sintaxe) NUNCA pode conter a solução ou regra de negócio específica do problema!
   - É ESTRITAMENTE PROIBIDO colocar regras de negócio do exercício dentro do código (ex: NUNCA escreva `medias[i] >= 7`, `aprovados++`, `exame++`, `reprovados++` ou `medias[i] > maior`).
   - O código DEVE ser 100% abstrato contendo APENAS a carcaça sintática simples com placeholders (`sua_condicao_maior`, `sua_condicao_aprovado`, `contadorAprovados++`).
   - Fórmulas e regras devem ser explicadas APENAS em texto/matemática, JAMAIS no código C++.

3. CÓDIGO CUMULATIVO E INCREMENTAL:
   - Em cada etapa nova, instrua o aluno a pegar o código que ele próprio escreveu na etapa anterior e construir em cima dele, enviando o código cumulativo atualizado.

4. ESTRUTURA OBRIGATÓRIA DE CADA MENSAGEM DE ETAPA:
   a) **Nome da Etapa Macro**: Ex: `📢 Etapa 1: Entrada de Dados e Boas Práticas`.
   b) **Justificativa Objetiva e Separação Didática de Estruturas**: Explique por que cada regra tem sua própria estrutura simples.
   c) **Explicação Lógica do Problema (Sem Código)**: Explique as regras e fórmulas em português/matemática.
   d) **Onde Implementar**: Explique em qual parte do código a nova lógica deve ser adicionada.
   e) **Código Genérico 100% Abstrato (Com Estruturas Simples e Desacopladas)**: Modelo sintático demonstrando a separação atômica por regra de negócio.
   f) **Instrução Direta**: Peça ao aluno para expandir seu código cumulativo.

5. CORREÇÃO DE ERROS (ZERO CÓDIGO NA RESPOSTA):
   - Se o código enviado contiver erros: explique objetivamente as falhas conceituais em texto puro.
   - REGRA ABSOLUTA: É ESTRITAMENTE PROIBIDO GERAR QUALQUER BLOCO DE CÓDIGO OU CÓDIGO DE CORREÇÃO NA SUA RESPOSTA.

{FEW_SHOT_PBL_EXAMPLES}
"""

def extract_previously_cited_sources(messages: List[Dict[str, str]]) -> set:
    cited_set = set()
    for m in messages:
        if m.get("role") in ["assistant", "bot"]:
            content = m.get("content", "")
            match = re.search(r"📚\s*\*\*Fonte\(s\) do Acervo:\*\*\s*(.*)", content)
            if match:
                sources_str = match.group(1)
                items = [item.strip() for item in sources_str.split(",") if item.strip()]
                for it in items:
                    cited_set.add(it)
    return cited_set

def generate_smart_fallback_response(messages: List[Dict[str, str]], user_message: str, all_retrieved: Optional[List[Dict[str, Any]]] = None) -> str:
    """
    Gera uma resposta didática e socrática como assistente IARA quando a API da OpenAI não está disponível
    (Modo Demonstração / Zero-Setup Local).
    """
    msg_lower = user_message.lower().strip()
    intent = detect_user_intent(user_message)
    
    if intent == "GREETING":
        return (
            "Olá! Sou a **IARA** (Inteligência Artificial de Raciocínio Algorítmico), sua tutora educacional para o ensino de programação e estruturas de dados.\n\n"
            "Estou aqui para apoiar o seu aprendizado de forma socrática, ajudando você a compreender a lógica dos algoritmos, corrigir erros em seu código e fixar conceitos fundamentais.\n\n"
            "💡 *Como posso te ajudar no estudo de algoritmos hoje? Você pode me enviar uma dúvida conceitual ou colar um trecho de código C++ / Python para analisarmos juntos!*"
        )
    
    rag_material_info = ""
    if all_retrieved and len(all_retrieved) > 0:
        first = all_retrieved[0]
        fn = first.get("filename", "Material de Algoritmos")
        loc = first.get("location") or first.get("title") or "Conceito Fundamental"
        content_snippet = first.get("content", "")
        rag_material_info = f"\n\n> 📚 **Referência do Material Didático da Turma (`{fn}` - {loc}):**\n\n{content_snippet[:350]}...\n"

    if any(k in msg_lower for k in ["while", "do while", "repetiço", "repeticao", "loop"]):
        return (
            "### 🧠 Entendendo o Laço `while` e Estruturas de Repetição\n\n"
            "O laço `while` é utilizado quando queremos repetir um bloco de comandos **enquanto uma condição booleana permanecer verdadeira**.\n\n"
            "```cpp\n"
            "int contador = 0;\n"
            "while (contador < 5) {\n"
            "    cout << \"Executando passo: \" << contador << endl;\n"
            "    contador++; // Atualização da variável de controle\n"
            "}\n"
            "```\n\n"
            "#### 🔍 Elementos Chave:\n"
            "1. **Inicialização:** Definição da variável de controle (`int contador = 0;`).\n"
            "2. **Condição de Parada:** Teste lógico avaliado antes de cada repetição (`contador < 5`).\n"
            "3. **Passo/Incremento:** Alteração da variável para que o loop termine eventualmente e não gere um **loop infinito**."
            + rag_material_info +
            "\n\n💬 **Pergunta para você exercitar:** O que aconteceria se a condição inicial fosse `contador > 5` em vez de `contador < 5`?"
        )
    
    elif any(k in msg_lower for k in ["for", "para"]):
        return (
            "### 🧠 Estrutura de Repetição `for`\n\n"
            "O laço `for` é ideal quando conhecemos previamente a quantidade exata de repetições necessárias.\n\n"
            "```cpp\n"
            "// Sintaxe: for (inicialização; condição; incremento)\n"
            "for (int i = 0; i < 10; i++) {\n"
            "    cout << \"Valor de i: \" << i << endl;\n"
            "}\n"
            "```\n\n"
            "#### 📌 Boas Práticas:\n"
            "- A variável de controle `i` tem escopo local dentro do bloco do `for`.\n"
            "- Os elementos de controle ficam agrupados no cabeçalho do laço, facilitando a leitura do código."
            + rag_material_info +
            "\n\n💬 **Desafio Socrático:** Como você reescreveria esse laço para contar em ordem decrescente (de 10 até 1)?"
        )
        
    elif any(k in msg_lower for k in ["vetor", "vetores", "array", "matriz"]):
        return (
            "### 🧠 Trabalhando com Vetores (Arrays)\n\n"
            "Um vetor é uma estrutura de dados homogênea e contígua na memória que permite armazenar múltiplos valores acessíveis por um índice numérico.\n\n"
            "```cpp\n"
            "int notas[5]; // Declara um vetor para 5 inteiros\n\n"
            "// Preenchendo o vetor:\n"
            "for (int i = 0; i < 5; i++) {\n"
            "    notas[i] = (i + 1) * 10;\n"
            "}\n"
            "```\n\n"
            "⚠️ **Atenção aos Índices:** Em C++ e na maioria das linguagens, os índices começam em **0** e vão até **N-1** (ex: de 0 a 4 para 5 elementos)."
            + rag_material_info +
            "\n\n💬 **Pergunta para reflexão:** Qual seria o resultado de tentar acessar `notas[5]` em um vetor de tamanho 5?"
        )
        
    elif any(k in msg_lower for k in ["if", "else", "condicional", "condicao"]):
        return (
            "### 🧠 Estruturas Condicionais (`if` / `else`)\n\n"
            "As estruturas condicionais permitem que o programa tome caminhos diferentes de execução com base em testes lógicos.\n\n"
            "```cpp\n"
            "int nota = 85;\n\n"
            "if (nota >= 60) {\n"
            "    cout << \"Aluno Aprovado!\" << endl;\n"
            "} else {\n"
            "    cout << \"Aluno em Recuperação.\" << endl;\n"
            "}\n"
            "```\n\n"
            "#### 💡 Dica de Raciocínio:\n"
            "Lembre-se da diferença entre o operador de atribuição (`=`) e o operador relacional de igualdade (`==`). Usar `=` dentro da condição do `if` é um erro comum de iniciantes!"
            + rag_material_info +
            "\n\n💬 **Quer praticar?** Tente incluir uma condição para verificar se o aluno tirou nota máxima (100) com um elogio especial!"
        )

    else:
        return (
            "### 🧠 Análise Didática de Raciocínio Algorítmico (IARA)\n\n"
            "Analisando sua pergunta no contexto de lógica de programação:\n\n"
            "1. **Entendimento da Demanda:** É fundamental mapear com clareza os dados de entrada, o processamento intermediário e a saída esperada.\n"
            "2. **Divisão do Problema:** Aplique o princípio da decomposição — resolva partes menores do algoritmo antes de juntar toda a solução.\n"
            "3. **Análise de Variáveis e Escopo:** Verifique se suas variáveis estão inicializadas com valores corretos antes da primeira leitura ou cálculo.\n"
            + rag_material_info +
            "\n\n💬 **Como podemos progredir?** Se desejar, me envie a sua tentativa de código ou me explique com suas palavras a lógica que você pretende utilizar para resolver esse exercício!"
        )

def generate_chat_response(messages: List[Dict[str, str]], user_message: str, class_id: Optional[str] = None) -> str:
    """
    Pipeline de Consulta RAG Adaptativo PBL Interativo IARA 6.0 com suporte a Múltiplas Turmas.
    """
    from bson import ObjectId
    class_doc = None
    subject_type = "programming"
    custom_guidelines = None
    class_name = ""
    rag_summary = ""
    if class_id:
        try:
            class_doc = classes_collection.find_one({"_id": ObjectId(class_id)})
            if class_doc:
                subject_type = class_doc.get("subject_type", "programming")
                custom_guidelines = class_doc.get("custom_guidelines")
                class_name = class_doc.get("name", "")
                rag_summary = class_doc.get("rag_summary")
                if not rag_summary:
                    rag_summary = update_class_rag_summary(class_id)
        except Exception as e:
            logger.error(f"Erro ao buscar turma com ID '{class_id}': {e}")

    from services.code_guardrail_service import detect_bypass_or_merge_request
    is_bypass_request = detect_bypass_or_merge_request(user_message)
    user_submitted_code = has_student_code(user_message)
    intent = detect_user_intent(user_message)
    logger.info(f"Pipeline RAG (Turma: {class_id}, Tipo: {subject_type}): Intenção = '{intent}', Código = {user_submitted_code}, Bypass = {is_bypass_request}")

    # 1. Busca de trechos no acervo RAG filtrando por turma (Base Conceitual e Livros)
    concept_chunks = search_concept_base(user_message, top_k=4, category=None, class_id=class_id)

    # 2. Busca no catálogo de exercícios (se aplicável)
    exercise_match = search_exercise_catalog(user_message, class_id=class_id)
    concepts_to_search = []
    if exercise_match:
        logger.info(f"Pipeline RAG PBL: Exercício clássico reconhecido: '{exercise_match.get('title')}'")
        concepts_to_search = exercise_match.get("concepts_involved", [])
        if not concepts_to_search:
            concepts_to_search = extract_concepts_from_exercise_text(exercise_match.get("content", ""))

    additional_chunks = []
    for concept in concepts_to_search:
        c_retrieved = search_concept_base(concept, top_k=3, category=None, class_id=class_id)
        additional_chunks.extend(c_retrieved)

    all_chunks = concept_chunks + additional_chunks

    # Deduplicação de trechos RAG
    all_retrieved = []
    seen_ids = set()
    for c in all_chunks:
        c_id = str(c.get("_id", c.get("title", "")))
        if c_id and c_id not in seen_ids:
            seen_ids.add(c_id)
            all_retrieved.append(c)

    client = get_openai_client()
    if not client:
        logger.info("Chave OpenAI não configurada. Acionando motor socrático fallback de demonstração.")
        return generate_smart_fallback_response(messages, user_message, all_retrieved)


    rag_context = ""
    citation_items = []
    if all_retrieved:
        rag_context = "\n--- CONCEITOS E MATERIAIS RECUPERADOS DO ACERVO DA TURMA (RAG) ---\n"
        for c in all_retrieved:
            fn = c.get("filename")
            loc = c.get("location") or c.get("title")
            rag_context += f"[Material: {fn} | Seção: {loc}]\n{c.get('content')}\n\n"
            if fn:
                citation_items.append(f"`{fn}` ({loc})" if loc else f"`{fn}`")

    unique_citations = sorted(list(set(citation_items)))
    previously_cited = extract_previously_cited_sources(messages)
    new_citations = [c for c in unique_citations if c not in previously_cited]

    # Construção do prompt instrucional dinâmico com HIERARQUIA DO ACERVO E FONTE DE PESQUISA
    BASE_RAG_KNOWLEDGE_PROMPT = f"""Você é IARA, a tutora virtual e assistente pedagógica da turma '{class_name if class_name else 'IARA'}'.

=== 🔴 REGRA SUPREMA: PESQUISA E EMBASAMENTO EM CONTEÚDO (ACERVO RAG vs PESQUISA INTERNET) ===

1. BASE PRINCIPAL DE PESQUISA (ACERVO RAG DA TURMA):
   - O acervo RAG disponibilizado pelo professor é sua fonte PRINCIPAL e PRIMÁRIA de consulta sobre o assunto da turma.
   - Sumário / Assuntos cobertos pela turma:
     {rag_summary if rag_summary else 'Acervo RAG da turma.'}

2. EXPANSÃO VIA PESQUISA EXTERNA (INTERNET / CONHECIMENTO GERAL):
   - Se o aluno fizer uma dúvida que TENHA RELAÇÃO com o assunto/sumário da turma indicado acima, porém os detalhes ou a resposta específica NÃO estiverem totalmente nos trechos recuperados do acervo RAG:
     * Você PODE E DEVE utilizar seu conhecimento e capacidade de pesquisa de IA para responder à dúvida do aluno de forma clara, precisa e didática.
     * Ao final da mensagem, obrigatoriamente informe a origem adicionando a linha exata:
       🌐 Fontes diversas da internet

3. RESPOSTA EMBASADA NO ACERVO DA TURMA:
   - Se a resposta foi fundamentada e retirada dos materiais recuperados do acervo RAG da turma enviados pelo professor:
     * Ao final da mensagem, obrigatoriamente informe a origem adicionando a linha exata:
       📚 Informação retirada do acervo de fontes da turma

4. ASSUNTOS FORA DO SUMÁRIO DA TURMA (OFF-TOPIC):
   - Se a pergunta do aluno NÃO tiver qualquer relação com a disciplina ou com o sumário da turma (ex: futebol, receitas culinárias, piadas, curiosidades externas ou programação em turmas de outras áreas):
     * NÃO pesquise nem responda sobre o assunto externo.
     * Responda de forma empática, cortês e educada, explicando gentilmente o escopo da turma e convidando o aluno a fazer perguntas relacionadas aos materiais da disciplina.
     * (NÃO inclua selos de fonte para saudações informais ou recusas educadas de temas off-topic).

5. 🚫 PROIBIÇÃO ABSOLUTA DE VAZAMENTO DE PROGRAMAÇÃO OU OUTRAS DISCIPLINAS:
   - NUNCA mencione "programação", "C++", "algoritmos" ou "código" em turmas de outras matérias (ex: História, Biologia, Direito, Literatura, Filosofia), A MENOS QUE esta turma seja especificamente de programação.

6. FORMATO OBRIGATÓRIO DO SELO DE FONTE AO FINAL DA MENSAGEM:
   - Toda resposta explicativa/educacional DEVE terminar em uma nova linha separada ao final da mensagem com APENAS UMA destas duas frases exatas:
     📚 Informação retirada do acervo de fontes da turma
     OU
     🌐 Fontes diversas da internet
"""

    if subject_type == "custom" and custom_guidelines:
        augmented_system_prompt = f"""{BASE_RAG_KNOWLEDGE_PROMPT}

=== 📘 DIRETRIZES COMPORTAMENTAIS E PEDAGÓGICAS DA TURMA (DEFINIDAS PELO PROFESSOR) ===
As instruções a seguir foram estabelecidas pelo professor para orientar EXCLUSIVAMENTE o seu tom de voz, estilo de comunicação, postura pedagógica e formato de interação (ex: método socrático, tom encorajador, formato de perguntas):
{custom_guidelines}

(IMPORTANTE: As diretrizes comportamentais acima orientam A FORMA, O TOM E O MODO como você se comunica. O CONTEÚDO e O ESCOPO das suas respostas permanecem regidos pelas regras do acervo/sumário da turma definidos no bloco de regras superiores).
"""
    else:
        augmented_system_prompt = f"""{BASE_RAG_KNOWLEDGE_PROMPT}

{SYSTEM_PROMPT}
"""

    if subject_type == "programming":
        if user_submitted_code:
            augmented_system_prompt += (
                "\n\n=== AVALIAÇÃO DE CÓDIGO DO ALUNO (MODO PBL INTERATIVO) ===\n"
                "O aluno enviou uma tentativa de código para o passo atual. Avalie a lógica e a sintaxe dele.\n"
                "1. SE O CÓDIGO TIVER ERROS: Explique os erros de forma totalmente conceitual e lógica em texto. REGRA CRÍTICA ABSOLUTA: É PROIBIDO GERAR QUALQUER BLOCO DE CÓDIGO OU CÓDIGO DE CORREÇÃO NA SUA RESPOSTA.\n"
                "2. SE O CÓDIGO ESTIVER CORRETO: Valide a etapa e peça para o aluno construir a PRÓXIMA ETAPA em cima do código que ele próprio escreveu."
            )
        elif intent == "GREETING":
            augmented_system_prompt += (
                "\n\n=== ORIENTAÇÃO DE SAUDAÇÃO ===\n"
                "O aluno enviou uma saudação ou conversa informal inicial.\n"
                f"Responda de forma breve, cortês e acolhedora, apresentando-se como IARA, a tutora virtual de programação da turma '{class_name if class_name else 'IARA'}', e perguntando em que pode ajudar nos estudos hoje."
            )
        elif intent == "CONCEPTUAL_QUESTION":
            augmented_system_prompt += (
                "\n\n=== DÚVIDA CONCEITUAL DE PROGRAMAÇÃO ===\n"
                "O aluno fez uma dúvida conceitual isolada sobre a matéria. Responda diretamente explicando o conceito com clareza pedagógica.\n"
                "Se a resposta for baseada no acervo RAG fornecido abaixo, adicione ao final: 📚 Informação retirada do acervo de fontes da turma\n"
                "Se for um conceito geral da disciplina expandido via IA, adicione ao final: 🌐 Fontes diversas da internet"
            )
        else:
            # EXERCÍCIO / DESAFIO DE PROGRAMAÇÃO (MODO PBL PASSO A PASSO OBRIGATÓRIO)
            augmented_system_prompt += (
                "\n\n=== MODO EXERCÍCIO DIDÁTICO (PBL PASSO A PASSO OBRIGATÓRIO) ===\n"
                "O aluno enviou um problema/exercício de programação ou solicitou a criação de um programa.\n"
                "Siga RIGOROSAMENTE o formato PBL interativo do SYSTEM_PROMPT e os FEW_SHOT_PBL_EXAMPLES:\n\n"
                "1. REGRA ABSOLUTA DE TRAVA DE CÓDIGO (CODE BRAKE):\n"
                "   - JAMAIS forneça o código completo da questão nem resolva o exercício para o aluno!\n"
                "   - Monte apenas a Etapa 1 por vez.\n\n"
                "2. ESTRUTURA DA MENSAGEM (OBRIGATÓRIA):\n"
                "   Desafio: [Breve resumo do enunciado]\n\n"
                "   ---\n"
                "   ### 📢 Etapa 1: [Nome da Etapa 1]\n\n"
                "   **Justificativa da Escolha Conceitual:**\n"
                "   [Explique em tópicos por que cada estrutura simples foi escolhida]\n\n"
                "   **Onde Implementar no Código:**\n"
                "   [Explique em qual parte do arquivo o código fica]\n\n"
                "   **Código Genérico (Template Sintático 100% Abstrato e Simples):**\n"
                "   ```cpp\n"
                "   // Use APENAS placeholders genéricos 100% abstratos como NOME_CONSTANTE, tipoVar, nomeVetor, sua_condicao.\n"
                "   // NUNCA COLOQUE VARIÁVEIS, NÚMEROS OU SOLUÇÃO DO ENUNCIADO DO ALUNO NO TEMPLATE!\n"
                "   ```\n\n"
                "   **Instrução:**\n"
                "   [Peça para o aluno escrever o código da Etapa 1 e enviar no chat para você avaliar]\n"
            )
    else:
        # Turmas Customizadas (Não-Programação)
        if intent == "GREETING":
            augmented_system_prompt += (
                "\n\n=== ORIENTAÇÃO DE SAUDAÇÃO ===\n"
                "O aluno enviou uma saudação ou conversa informal inicial.\n"
                f"Responda de forma breve, cortês e acolhedora, apresentando-se como IARA, a tutora virtual da turma '{class_name if class_name else 'IARA'}', e perguntando em que pode ajudar nos estudos hoje."
            )
        elif not all_retrieved:
            augmented_system_prompt += (
                "\n\n=== ORIENTAÇÃO DE RESPOSTA (SEM CONTEXTO RAG DIRETO) ===\n"
                "Nenhum documento do acervo RAG foi retornado diretamente para esta consulta específica nesta turma.\n"
                "Siga rigorosamente estas instruções:\n"
                f"1. SE A PERGUNTA TIVER RELAÇÃO COM O SUMÁRIO DA TURMA ('{rag_summary}'): "
                "responda à dúvida do aluno de forma didática e completa utilizando seu conhecimento de IA/internet, e finalize obrigatoriamente a mensagem com a linha exata:\n"
                "🌐 Fontes diversas da internet\n\n"
                "2. SE FOR UM ASSUNTO TOTALMENTE FORA DO SUMÁRIO DA TURMA (off-topic, ex: esportes, receitas, política, piadas ou programação fora da turma de computação): "
                "reconheça o comentário do aluno de forma amigável e empática. Explique com gentileza que seu foco é exclusivo nos conteúdos e materiais desta turma e convide-o a fazer uma pergunta sobre a matéria. (Não adicione selo de fonte)."
            )
        else:
            augmented_system_prompt += (
                "\n\n=== MODO DÚVIDA / CONSULTA DA DISCIPLINA ===\n"
                "1. Se os trechos do acervo RAG fornecidos abaixo responderem à dúvida: utilize-os e finalize a mensagem com a linha exata:\n"
                "📚 Informação retirada do acervo de fontes da turma\n"
                "2. Se a dúvida tiver relação com o sumário da turma mas os trechos recuperados não contiverem a resposta completa: use seu conhecimento de IA para responder e finalize a mensagem com a linha exata:\n"
                "🌐 Fontes diversas da internet"
            )

    if rag_context:
        augmented_system_prompt += f"\n\n=== BASE CONCEITUAL E MATERIAIS DA TURMA (RAG) ===\n{rag_context}"

    recent_history = [m for m in messages if m.get("role") != "system"][-15:]
    if not recent_history or recent_history[-1].get("content") != user_message:
        recent_history.append({"role": "user", "content": user_message})

    final_messages = [{"role": "system", "content": augmented_system_prompt}, *recent_history]

    try:
        from config import OPENAI_MODEL
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=final_messages,
            temperature=0.4 if (intent in ["CONCEPTUAL_QUESTION", "GREETING", "GENERAL_QUERY"] or not all_retrieved or subject_type != "programming") else 0.3,
            max_tokens=1000
        )
        reply_content = response.choices[0].message.content.strip()

        if subject_type == "programming":
            if user_submitted_code and ("erro" in reply_content.lower() or "incorreto" in reply_content.lower() or "ajustar" in reply_content.lower()):
                reply_content = strip_code_blocks(reply_content)
            elif all_retrieved:
                from services.code_guardrail_service import apply_code_brake, sanitize_specific_domain_logic
                reply_content = apply_code_brake(reply_content, all_retrieved, new_citations)
                reply_content = sanitize_specific_domain_logic(reply_content)

        return reply_content
    except Exception as e:
        logger.error(f"Erro ao chamar OpenAI: {e}. Acionando motor socrático de demonstração.")
        return generate_smart_fallback_response(messages, user_message, all_retrieved)

def generate_chat_title(user_message: str) -> Optional[str]:
    client = get_openai_client()
    if not client:
        clean_title = re.sub(r'[^\w\s]', '', user_message).strip()
        words = clean_title.split()
        if len(words) > 0:
            return " ".join(words[:4]).capitalize()
        return "Dúvida de Programação"
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Gere um título forte, curto e explicativo para este chat baseado na mensagem do usuário. Retorne apenas o título, sem aspas, com no máximo 30 caracteres."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=50
        )
        title = response.choices[0].message.content.strip().replace('"', '').replace("'", "")
        return title if title else "Dúvida de Programação"
    except Exception as e:
        logger.error(f"Erro ao gerar título: {e}")
        clean_title = re.sub(r'[^\w\s]', '', user_message).strip()
        words = clean_title.split()
        if len(words) > 0:
            return " ".join(words[:4]).capitalize()
        return "Dúvida de Programação"
