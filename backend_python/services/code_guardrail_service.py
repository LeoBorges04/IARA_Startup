import re
import logging
from difflib import SequenceMatcher
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

POLITE_REFUSAL = "Como tutora IARA, não posso fornecer o código completo do exercício."

BYPASS_KEYWORDS = [
    "juntar", "junte", "código completo", "codigo completo", "programa completo", 
    "código inteiro", "codigo inteiro", "unir as partes", "unir os codigos", 
    "mostrar tudo", "código final", "codigo final", "juntar as etapas",
    "junta tudo", "me dá o código", "me da o codigo", "gera o arquivo completo",
    "unir tudo", "código todo", "codigo todo"
]

def detect_bypass_or_merge_request(user_message: str) -> bool:
    """Detecta se o usuário solicitou a junção de código ou a entrega do programa completo."""
    msg_lower = user_message.lower().strip()
    return any(k in msg_lower for k in BYPASS_KEYWORDS)

# Frases e seções motivacionais / conclusões prolixas a serem filtradas
DISALLOWED_PATTERNS = [
    r"você consegue.*",
    r"bons estudos.*",
    r"boa sorte.*",
    r"dica motivacional.*",
    r"boas práticas:.*",
    r"em resumo,.*",
    r"conclusão:.*",
    r"conclusao:.*",
    r"lembre-se de que a prática faz a perfeição.*",
    r"continue praticando.*"
]

def extract_code_blocks(text: str) -> List[str]:
    """Extrai todos os blocos de código demarcados por ```...``` na resposta."""
    pattern = r"```(?:\w+)?\n([\s\S]*?)```"
    return re.findall(pattern, text)

def is_preassembled_code(code_str: str) -> bool:
    """
    Analisa a densidade estrutural do código para verificar se ele forma uma solução pré-montada ou completa.
    Retorna False se o código for um template genérico/abstrato com placeholders.
    """
    code_lower = code_str.lower()
    
    # Se contiver placeholders genéricos explícitos, é um template sintático didático e NÃO vazamento de código completo
    placeholders = [
        "nome_constante", "nomevetor", "tipovar", "variavelmaior", "variavelmenor", 
        "nomevariavel", "condicao", "sua_condicao", "sua_acao", "contador1", "contador2", 
        "contadoraprovados", "tipodado", "limite"
    ]
    if any(ph in code_lower for ph in placeholders):
        return False

    # Marcadores de estruturas principais
    has_main = bool(re.search(r'\b(int\s+main|void\s+main|def\s+main|public\s+static\s+void\s+main)\b', code_lower))
    has_loop = bool(re.search(r'\b(for|while|do)\b', code_lower))
    has_cond = bool(re.search(r'\b(if|else|switch|case)\b', code_lower))
    has_struct_or_func = bool(re.search(r'\b(struct|class|def|void|int|float|double|char)\b', code_lower))
    has_io = bool(re.search(r'\b(cin|cout|printf|scanf|print|input)\b', code_lower))
    
    structural_count = sum([has_main, has_loop, has_cond, has_struct_or_func, has_io])
    
    if has_main and (has_loop or has_cond):
        return True
    
    if structural_count >= 3:
        return True
        
    return False

def calculate_similarity(s1: str, s2: str) -> float:
    """Calcula a similaridade textual/estrutural entre duas strings de código."""
    norm1 = re.sub(r'\s+', ' ', s1).strip()
    norm2 = re.sub(r'\s+', ' ', s2).strip()
    return SequenceMatcher(None, norm1, norm2).ratio()

def is_matching_rag_template(code_block: str, rag_code_chunks: List[Dict[str, Any]]) -> bool:
    """
    Verifica se o bloco de código gerado pela OpenAI coincide de forma idêntica (ou quase idêntica)
    com um único template genérico recuperado do acervo RAG.
    """
    if not rag_code_chunks:
        return False
        
    for chunk in rag_code_chunks:
        content = chunk.get("content", "")
        rag_blocks = extract_code_blocks(content)
        target_texts = rag_blocks if rag_blocks else [content]
        
        for rag_text in target_texts:
            similarity = calculate_similarity(code_block, rag_text)
            if similarity >= 0.85:
                return True
                
    return False

def clean_fluff_text(text: str) -> str:
    """Remove textos motivacionais prolixos, dicas de boas práticas longas e conclusões de final de documento."""
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line_lower = line.lower().strip()
        skip = False
        for pat in DISALLOWED_PATTERNS:
            if re.search(pat, line_lower):
                skip = True
                break
        if not skip:
            cleaned_lines.append(line)
            
    return "\n".join(cleaned_lines).strip()

def sanitize_specific_domain_logic(text: str) -> str:
    """
    Substitui apenas comparações numéricas específicas de negócio (ex: 'medias[i] >= 7')
    por placeholders abstratos (ex: 'sua_condicao_1'), sem alterar iteradores de laço (ex: 'i < NOME_CONSTANTE').
    """
    code_blocks = extract_code_blocks(text)
    if not code_blocks:
        return text

    new_text = text
    for cb in code_blocks:
        cb_sanitized = cb
        # Preserva laços for (int i = 0; i < NOME_CONSTANTE; i++) ou (int i = 0; i < TAM; i++)
        # Substitui apenas condicionais específicas de negócio com números ou variáveis de domínio
        cb_sanitized = re.sub(r'if\s*\((?!\s*i\s*<|\s*j\s*<)(.*?)\)', r'if (sua_condicao)', cb_sanitized)
        cb_sanitized = re.sub(r'(\b(aprovados|reprovados|exame)\b\s*(\+\+|--|\+=|=).*?;)', r'contador1++;', cb_sanitized)
        
        if cb_sanitized != cb:
            new_text = new_text.replace(cb, cb_sanitized)

    return new_text
    if not raw_content:
        return ""
        
    # Se já possui bloco de código Markdown, extrai apenas o bloco de código
    code_blocks = extract_code_blocks(raw_content)
    if code_blocks:
        lang_match = re.search(r"```(\w+)?\n", raw_content)
        lang = lang_match.group(1) if lang_match and lang_match.group(1) else "cpp"
        return f"```{lang}\n{code_blocks[0].strip()}\n```"

    # Se possui a seção "Código:", extrai o trecho exato de código
    code_match = re.search(r"Código:\s*\n?([\s\S]*?)(?=\n\s*Observações:|\n\s*Observacoes:|$)", raw_content, re.IGNORECASE)
    if code_match:
        code_text = code_match.group(1).strip()
        if code_text and ("int " in code_text or "for " in code_text or "if " in code_text or "cin " in code_text or "cout " in code_text or "struct " in code_text or "void " in code_text or "=" in code_text):
            return f"```cpp\n{code_text}\n```"

    # Se for texto de prosa de PDF sem código real, retorna string vazia
    return ""

def extract_identified_structures(openai_response: str) -> str:
    """
    Extrai a explicação das estruturas e do passo a passo didático identificados pela OpenAI,
    removendo qualquer bloco de código resolvido gerado por ela.
    """
    # 1. Remove blocos de código
    text_without_code = re.sub(r"```(?:\w+)?\n[\s\S]*?```", "", openai_response).strip()
    
    # 2. Remove negações repetidas do início
    if text_without_code.startswith(POLITE_REFUSAL):
        text_without_code = text_without_code[len(POLITE_REFUSAL):].strip()
    elif text_without_code.startswith("Como tutora IARA"):
        text_without_code = re.sub(r"^Como tutora IARA[^\n]*\n*", "", text_without_code).strip()
        
    # 3. Limpa rodapés e textos prolixos
    text_without_code = re.sub(r"📚.*$", "", text_without_code).strip()
    return clean_fluff_text(text_without_code)

def parse_openai_topics(openai_response: str) -> List[Dict[str, str]]:
    """
    Divide a resposta da OpenAI em tópicos/seções individuais baseando-se em listas numeradas ou títulos.
    Cada item retornado contém {'title': str, 'description': str}.
    """
    clean_text = extract_identified_structures(openai_response)
    
    topic_pattern = r"(?:^|\n)(?:###?\s*|\*\*\d+[\.\)]\s*|\d+[\.\)]\s*)([^\n]+)"
    matches = list(re.finditer(topic_pattern, clean_text))
    
    topics = []
    if matches:
        for idx, match in enumerate(matches):
            start = match.end()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(clean_text)
            
            raw_title = match.group(1).replace("**", "").strip()
            # Limpa prefixos numéricos repetidos (ex: "1. ", "1.1 ", "1. 1. ")
            clean_title = re.sub(r"^[\d\.\s\-]+", "", raw_title).strip()
            if not clean_title:
                clean_title = raw_title
                
            description = clean_text[start:end].strip()
            
            topics.append({
                "title": clean_title,
                "description": description
            })
    else:
        topics.append({
            "title": "Estruturas Necessárias",
            "description": clean_text
        })
        
    return topics

def build_modular_topic_response(topics_data: List[Dict[str, Any]], unique_citations: List[str]) -> str:
    """
    Monta a resposta modular concatenada por tópico.
    Cada tópico possui seu título, explicação didática e seu próprio 'Exemplo de sintaxe:' do RAG.
    """
    parts = [POLITE_REFUSAL]
    parts.append("Para resolver esta tarefa, vamos analisar as estruturas necessárias passo a passo:")
    
    for idx, t in enumerate(topics_data, start=1):
        title = t.get("title", f"Estrutura {idx}")
        desc = t.get("description", "")
        template = t.get("syntax_template", "")
        
        section = [f"### {idx}. {title}"]
        if desc:
            section.append(desc)
            
        if template:
            section.append(f"**Exemplo de sintaxe:**\n\n{template}")
            
        parts.append("\n\n".join(section))
        
    final_output = "\n\n".join(parts)
    return final_output

def get_best_syntax_template(rag_code_chunks: List[Dict[str, Any]]) -> str:
    """Busca o bloco de código/sintaxe genérica limpo e sem metadados mais adequado entre os chunks do acervo."""
    if not rag_code_chunks:
        return ""
        
    for chunk in rag_code_chunks:
        raw_content = chunk.get("content", "").strip()
        sanitized = sanitize_rag_chunk_content(raw_content)
        if sanitized:
            return sanitized
            
    return ""

CANONICAL_ATOMIC_TEMPLATES = {
    "VETOR": "```cpp\n// Declaração e acesso a vetor numérico:\ntipo nomeVetor[TAMANHO];\nnomeVetor[indice] = valor;\n```",
    "MATRIZ": "```cpp\n// Declaração de matriz bidimensional:\ntipo matriz[LINHAS][COLUNAS];\nmatriz[i][j] = valor;\n```",
    "LOOP": "```cpp\n// Estrutura de repetição para iterar N vezes:\nfor (int i = 0; i < limite; i++) {\n    // Código a ser repetido\n}\n```",
    "CONDICIONAL": "```cpp\n// Estrutura condicional para teste de expressão booleana:\nif (condicao) {\n    // Bloco executado se a condição for verdadeira\n}\n```",
    "CONTADOR": "```cpp\n// Variável contadora para incremento de ocorrências:\ncontador++; // Equivalente a: contador = contador + 1;\n```",
    "ACUMULADOR": "```cpp\n// Variável acumuladora para cálculo de somatório:\nsoma += valor; // Equivalente a: soma = soma + valor;\n```",
    "MAIOR_MENOR": "```cpp\n// Estrutura de atualização de maior ou menor valor:\nif (valor > maior) {\n    maior = valor;\n}\n```",
    "ENTRADA_SAIDA": "```cpp\n// Funções de entrada e saída padrão:\ncin >> variavel;\ncout << variavel << endl;\n```",
    "FUNCAO": "```cpp\n// Declaração de função com parâmetro e retorno:\nint minhaFuncao(int parametro) {\n    return parametro * 2;\n}\n```"
}

def detect_atomic_domain_tag(topic_title: str, topic_desc: str = "") -> str:
    """Classifica o tópico em exatamente 1 Tag de Domínio Atômica baseando-se em palavras-chave."""
    text = f"{topic_title} {topic_desc}".lower()
    
    if any(k in text for k in ["contar", "contador", "quantidade de", "contagem"]):
        return "CONTADOR"
    elif any(k in text for k in ["maior", "menor", "máximo", "mínimo"]):
        return "MAIOR_MENOR"
    elif any(k in text for k in ["somar", "soma", "acumular", "acumulador", "total"]):
        return "ACUMULADOR"
    elif any(k in text for k in ["vetor", "array", "elemento", "médias dos alunos", "armazenar médias"]):
        return "VETOR"
    elif any(k in text for k in ["matriz", "bidimensional", "linha", "coluna"]):
        return "MATRIZ"
    elif any(k in text for k in ["loop", "laço", "for", "while", "repetição", "percorrer", "iterar"]):
        return "LOOP"
    elif any(k in text for k in ["if", "else", "condicional", "condição", "aprovado", "verificar", "testar"]):
        return "CONDICIONAL"
    elif any(k in text for k in ["função", "método", "parâmetro", "retorno"]):
        return "FUNCAO"
    elif any(k in text for k in ["cin", "cout", "printf", "scanf", "ler", "exibir", "mostrar", "imprimir", "entrada", "saída"]):
        return "ENTRADA_SAIDA"
        
    return "CONDICIONAL"

def extract_chunk_metadata_fields(content: str) -> Dict[str, str]:
    """Extrai os campos Título, Categoria e Subcategoria de um chunk estruturado do RAG."""
    title_match = re.search(r"Título:\s*(.*)", content, re.IGNORECASE)
    subcat_match = re.search(r"Subcategoria:\s*(.*)", content, re.IGNORECASE)
    cat_match = re.search(r"Categoria:\s*(.*)", content, re.IGNORECASE)
    
    return {
        "title": title_match.group(1).strip() if title_match else "",
        "subcategoria": subcat_match.group(1).strip() if subcat_match else "",
        "categoria": cat_match.group(1).strip() if cat_match else ""
    }

def calculate_field_match_score(topic_title: str, chunk_content: str) -> float:
    """
    Calcula a pontuação de correspondência comparando o título do tópico com a Subcategoria, Título e Conteúdo do chunk.
    """
    fields = extract_chunk_metadata_fields(chunk_content)
    chunk_title = fields["title"].lower()
    chunk_subcat = fields["subcategoria"].lower()
    t_lower = topic_title.lower()
    c_lower = chunk_content.lower()
    
    score = 0.0
    if chunk_subcat:
        if chunk_subcat in t_lower or t_lower in chunk_subcat:
            score += 4.0
        else:
            score += SequenceMatcher(None, t_lower, chunk_subcat).ratio() * 2.5

    if chunk_title:
        if chunk_title in t_lower or t_lower in chunk_title:
            score += 4.0
        else:
            score += SequenceMatcher(None, t_lower, chunk_title).ratio() * 2.5
            
    words = [w for w in re.split(r"\W+", t_lower) if len(w) > 3]
    for w in words:
        if w in c_lower:
            score += 1.0

    return score

def get_best_syntax_template_for_topic(topic_title: str, candidate_chunks: List[Dict[str, Any]], fallback_template: str = "") -> str:
    """
    Classifica o tópico na sua Tag Atômica e resgata o chunk mais compatível do RAG.
    Se o RAG trouxer ruído ou chunk incompatível, retorna o Template Canônico Atômico da tag.
    """
    domain_tag = detect_atomic_domain_tag(topic_title)
    canonical = CANONICAL_ATOMIC_TEMPLATES.get(domain_tag, "")
    
    if not candidate_chunks:
        return canonical if canonical else fallback_template

    best_score = -1.0
    best_chunk = None

    for chunk in candidate_chunks:
        content = chunk.get("content", "").strip()
        score = calculate_field_match_score(topic_title, content)
        if score > best_score:
            best_score = score
            best_chunk = content

    if best_chunk and best_score > 2.0:
        sanitized = sanitize_rag_chunk_content(best_chunk)
        if sanitized:
            return sanitized

    return canonical if canonical else fallback_template

def apply_code_brake(response_text: str, rag_code_chunks: List[Dict[str, Any]], unique_citations: List[str]) -> str:
    """
    Sistema de Freio de Segurança:
    SÓ intercepta e reformata se a OpenAI tiver gerado um CÓDIGO COMPLETO PRÉ-MONTADO / RESOLVIDO.
    Se a resposta for conceitual ou contiver apenas trechos genéricos, preserva a resposta natural da OpenAI.
    """
    code_blocks = extract_code_blocks(response_text)
    
    needs_brake = False
    if code_blocks:
        for cb in code_blocks:
            if is_preassembled_code(cb):
                needs_brake = True
                break

    # Se a OpenAI respondeu de forma didática e sem vazamento de código completo, mantém a resposta original!
    if not needs_brake:
        return response_text

    logger.warning("FREIO DE SEGURANÇA ATIVADO: Vazamento de código pré-montado detectado. Reformatando por tópicos.")

    parsed_topics = parse_openai_topics(response_text)
    # Filtra meta-tópicos informativos que não requerem código (ex: Dicas, Observações, Conclusão)
    ignored_meta_titles = ["dicas", "dica", "observações", "observacoes", "resumo", "estrutura do programa", "definições e inclusões", "conclusão", "conclusao"]

    try:
        from services.rag_service import search_relevant_chunks
        for t in parsed_topics:
            t_title = t.get("title", "")
            t_desc = t.get("description", "")
            t_title_lower = t_title.lower().strip()

            if any(meta in t_title_lower for meta in ignored_meta_titles):
                t["syntax_template"] = ""
                continue

            if t_title:
                domain_tag = detect_atomic_domain_tag(t_title, t_desc)
                topic_candidates = search_relevant_chunks(t_title, top_k=5, category=None)
                if not topic_candidates:
                    topic_candidates = rag_code_chunks
                    
                t_template = get_best_syntax_template_for_topic(t_title, topic_candidates, CANONICAL_ATOMIC_TEMPLATES.get(domain_tag, ""))
                t["syntax_template"] = t_template
            else:
                t["syntax_template"] = ""
    except Exception as e:
        logger.error(f"Erro ao buscar templates RAG específicos por tópico: {e}")
        for t in parsed_topics:
            t["syntax_template"] = ""

    return build_modular_topic_response(parsed_topics, unique_citations)
