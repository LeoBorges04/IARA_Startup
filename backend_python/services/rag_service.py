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
from database import exercise_catalog_collection, concept_base_collection

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

def ingest_exercise_catalog(filename: str, content: Optional[str] = None, file_path: Optional[str] = None) -> int:
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
    logger.info(f"Base 1 (Exercícios): Gerando embeddings para {len(chunks_text)} documentos de '{filename}'...")
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
            "category": "exercise"
        })

    if docs_to_insert:
        exercise_catalog_collection.delete_many({"filename": filename})
        result = exercise_catalog_collection.insert_many(docs_to_insert)
        return len(result.inserted_ids)
    return 0

def ingest_concept_base(filename: str, content: Optional[str] = None, file_path: Optional[str] = None, category: str = "concept") -> int:
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
    logger.info(f"Base 2 (Conceitual): Gerando embeddings para {len(chunks_text)} documentos de '{filename}'...")
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
            "category": category
        })

    if docs_to_insert:
        concept_base_collection.delete_many({"filename": filename})
        document_chunks_collection.delete_many({"filename": filename})
        
        concept_base_collection.insert_many(docs_to_insert)
        result = document_chunks_collection.insert_many(docs_to_insert)
        return len(result.inserted_ids)
    return 0

def ingest_document(filename: str, content: Optional[str] = None, file_path: Optional[str] = None, category: str = "concept") -> int:
    """Roteador principal de ingestão."""
    if category == "exercise":
        return ingest_exercise_catalog(filename, content=content, file_path=file_path)
    else:
        return ingest_concept_base(filename, content=content, file_path=file_path, category=category)

def cosine_similarity(a: List[float], b: List[float]) -> float:
    vec_a = np.array(a, dtype=np.float32)
    vec_b = np.array(b, dtype=np.float32)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(vec_a, vec_b) / (norm_a * norm_b))

def search_exercise_catalog(query: str) -> Optional[Dict[str, Any]]:
    """Busca o exercício correspondente na Base 1 (Catálogo de Exercícios)."""
    query_vector = generate_embedding(query)
    all_docs = list(exercise_catalog_collection.find({}, {"filename": 1, "title": 1, "content": 1, "concepts_involved": 1, "embedding": 1}))
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

    return best_doc if (best_doc and best_score > 0.2) else None

def search_concept_base(query: str, top_k: int = 3, category: Optional[str] = None) -> List[Dict[str, Any]]:
    """Busca tópicos conceituais e livros acervados na Base 2 e no acervo de documentos."""
    query_vector = generate_embedding(query)
    filter_query = {}
    if category:
        filter_query["category"] = category

    docs_concept = list(concept_base_collection.find(filter_query, {"filename": 1, "title": 1, "location": 1, "content": 1, "embedding": 1, "category": 1}))
    docs_books = list(document_chunks_collection.find(filter_query, {"filename": 1, "title": 1, "location": 1, "content": 1, "embedding": 1, "category": 1}))

    all_docs = docs_concept + docs_books
    if not all_docs:
        return []

    scored_docs = []
    for doc in all_docs:
        emb = doc.get("embedding")
        if emb:
            score = cosine_similarity(query_vector, emb)
            scored_docs.append((score, doc))

    scored_docs.sort(key=lambda x: x[0], reverse=True)
    return [doc for score, doc in scored_docs[:top_k] if score > 0.15]

def search_relevant_chunks(query: str, top_k: int = 4, category: Optional[str] = None) -> List[Dict[str, Any]]:
    """Wrapper para compatibilidade."""
    return search_concept_base(query, top_k=top_k, category=category)

def detect_user_intent(user_message: str) -> str:
    """
    Detecta se o usuário está fazendo uma DÚVIDA PONTUAL/CONCEITUAL
    ou solicitando a estrutura para um NOVO EXERCÍCIO.
    """
    msg_lower = user_message.lower().strip()
    conceptual_keywords = [
        "por que", "porque", "qual a diferença", "qual é a diferença", 
        "o que é", "o que faz", "como funciona", "para que serve",
        "dúvida", "duvida", "não entendi", "nao entendi", "explique"
    ]
    is_conceptual = any(k in msg_lower for k in conceptual_keywords)
    has_exercise_prompt = any(k in msg_lower for k in ["faça um programa", "crie um algoritmo", "escreva um código", "como fazer um programa", "como implementar", "exercício", "desafio"])
    
    if is_conceptual and not has_exercise_prompt:
        return "CONCEPTUAL_QUESTION"
    return "EXERCISE"

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

SYSTEM_PROMPT = f"""Você é IARA, uma tutora virtual de programação baseada em Aprendizagem Baseada em Problemas (PBL Interativo).
Sua comunicação é ESTRITAMENTE OBJETIVA, DIRETA E CONCISA. É PROIBIDO o uso de frases motivacionais prolixas, saudações longas ou emojis.

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

def generate_chat_response(messages: List[Dict[str, str]], user_message: str) -> str:
    """
    Pipeline de Consulta RAG Adaptativo PBL Interativo IARA 6.0.
    """
    client = get_openai_client()
    if not client:
        return "Erro: Chave de API da OpenAI não configurada ou inválida no servidor."

    from services.code_guardrail_service import detect_bypass_or_merge_request
    is_bypass_request = detect_bypass_or_merge_request(user_message)
    user_submitted_code = has_student_code(user_message)
    intent = detect_user_intent(user_message)
    logger.info(f"Pipeline RAG PBL: Intenção = '{intent}', Código do Aluno = {user_submitted_code}, Pedido de Junção/Bypass = {is_bypass_request}")

    # Se for uma dúvida pontual/conceitual sem submissão de código
    if intent == "CONCEPTUAL_QUESTION" and not user_submitted_code:
        concept_chunks = search_concept_base(user_message, top_k=4, category=None)
        rag_context = ""
        citation_items = []
        if concept_chunks:
            rag_context = "\n--- CONCEITOS E LIVROS RECUPERADOS DO ACERVO (RAG) ---\n"
            for c in concept_chunks:
                fn = c.get("filename")
                loc = c.get("location") or c.get("title")
                rag_context += f"[Material: {fn} | Seção: {loc}]\n{c.get('content')}\n\n"
                if fn:
                    citation_items.append(f"`{fn}` ({loc})" if loc else f"`{fn}`")

        unique_citations = sorted(list(set(citation_items)))
        previously_cited = extract_previously_cited_sources(messages)
        new_citations = [c for c in unique_citations if c not in previously_cited]

        prompt_instruction = (
            f"{SYSTEM_PROMPT}\n\nO aluno está fazendo uma dúvida pontual. Responda DIRETAMENTE com clareza conceitual e objetividade humana. "
            "Se o acervo contiver a explicação, embase-se nele. Caso contrário, use seu conhecimento de IA para explicar conceitualmente no contexto do aluno."
        )
        if rag_context:
            prompt_instruction += f"\n\n=== CONTEXTO DOS LIVROS (RAG) ===\n{rag_context}"

        recent_history = [m for m in messages if m.get("role") != "system"][-15:]
        final_messages = [{"role": "system", "content": prompt_instruction}, *recent_history]

        try:
            from config import OPENAI_MODEL
            response = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=final_messages,
                temperature=0.4,
                max_tokens=800
            )
            reply = response.choices[0].message.content.strip()
            return reply
        except Exception as e:
            logger.error(f"Erro ao responder dúvida pontual: {e}")
            return f"Desculpe, ocorreu um erro: {str(e)}"

    # Caso seja um Desafio de Exercício ou Avaliação de Código do Aluno (PBL Mode)
    exercise_match = search_exercise_catalog(user_message)
    concepts_to_search = []
    
    if exercise_match:
        logger.info(f"Pipeline RAG PBL: Exercício clássico reconhecido: '{exercise_match.get('title')}'")
        concepts_to_search = exercise_match.get("concepts_involved", [])
        if not concepts_to_search:
            concepts_to_search = extract_concepts_from_exercise_text(exercise_match.get("content", ""))

    if not concepts_to_search:
        concepts_to_search = [user_message]

    concept_chunks = []
    for concept in concepts_to_search:
        c_retrieved = search_concept_base(concept, top_k=3, category=None)
        concept_chunks.extend(c_retrieved)

    if not concept_chunks:
        concept_chunks = search_concept_base(user_message, top_k=4, category=None)

    all_retrieved = []
    seen_ids = set()
    for c in concept_chunks:
        c_id = str(c.get("_id", c.get("title")))
        if c_id not in seen_ids:
            seen_ids.add(c_id)
            all_retrieved.append(c)

    citation_items = []
    for c in all_retrieved:
        fn = c.get("filename")
        loc = c.get("location") or c.get("title")
        if fn:
            citation_items.append(f"`{fn}` ({loc})" if loc else f"`{fn}`")

    unique_citations = sorted(list(set(citation_items)))
    previously_cited = extract_previously_cited_sources(messages)
    new_citations = [c for c in unique_citations if c not in previously_cited]

    rag_context = ""
    if all_retrieved:
        rag_context += "\n--- CONTEXTO DOS LIVROS E CONCEITOS DO ACERVO (RAG) ---\n"
        for c in all_retrieved:
            rag_context += f"[Material: {c.get('filename')} | Seção: {c.get('title')}]\n{c.get('content')}\n\n"

    augmented_system_prompt = SYSTEM_PROMPT
    if user_submitted_code:
        augmented_system_prompt += (
            "\n\n=== ATENÇÃO: AVALIAÇÃO DE CÓDIGO DO ALUNO ===\n"
            "O aluno enviou uma tentativa de código para o passo atual. Avalie a lógica e a sintaxe dele.\n"
            "1. SE O CÓDIGO TIVER ERROS: Explique os erros de forma totalmente conceitual e lógica em texto. REGRA CRÍTICA: NÃO GERAR NENHUM CÓDIGO DE CORREÇÃO.\n"
            "2. SE O CÓDIGO ESTIVER CORRETO: Valide o passo e peça para ele fazer o PRÓXIMO PASSO."
        )

    if rag_context:
        augmented_system_prompt += f"\n\n=== BASE CONCEITUAL E LIVROS (RAG) ===\n{rag_context}"

    recent_history = [m for m in messages if m.get("role") != "system"][-15:]
    final_messages = [{"role": "system", "content": augmented_system_prompt}, *recent_history]

    try:
        from config import OPENAI_MODEL
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=final_messages,
            temperature=0.3,
            max_tokens=1000
        )
        reply_content = response.choices[0].message.content.strip()
        
        # Se for avaliação de código e a IARA tiver gerado algum código por erro, remove o bloco de código
        if user_submitted_code and ("erro" in reply_content.lower() or "incorreto" in reply_content.lower() or "ajustar" in reply_content.lower()):
            reply_content = strip_code_blocks(reply_content)
        else:
            from services.code_guardrail_service import apply_code_brake, sanitize_specific_domain_logic
            reply_content = apply_code_brake(reply_content, all_retrieved, new_citations)
            reply_content = sanitize_specific_domain_logic(reply_content)
        return reply_content
    except Exception as e:
        logger.error(f"Erro ao chamar OpenAI no modo PBL: {e}")
        return f"Desculpe, ocorreu um erro ao gerar a resposta: {str(e)}"

def generate_chat_title(user_message: str) -> Optional[str]:
    client = get_openai_client()
    if not client:
        return None
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
        return title if title else None
    except Exception as e:
        logger.error(f"Erro ao gerar título: {e}")
        return None
