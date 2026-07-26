import os
import sys
from services.rag_service import extract_text_from_file, ingest_document
from database import check_connection

def process_directory(directory_path: str, category: str = "concept"):
    if not os.path.exists(directory_path):
        print(f"Diretório '{directory_path}' não encontrado.")
        return

    check_connection()
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    print(f"Encontrados {len(files)} arquivos no diretório '{directory_path}' (Categoria: {category})...")

    for filename in files:
        file_path = os.path.join(directory_path, filename)
        try:
            count = ingest_document(filename=filename, file_path=file_path, category=category)
            if count > 0:
                print(f"✅ Arquivo '{filename}' ingerido -> {count} chunks criados com metadados.")
            else:
                print(f"⚠️ Arquivo '{filename}' vazio ou não pôde ser lido.")
        except Exception as e:
            print(f"❌ Erro ao ingerir '{filename}': {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
        cat = sys.argv[2] if len(sys.argv) > 2 else "concept"
        process_directory(target_dir, cat)
    else:
        # Por padrão processa a pasta local de exemplos de código se existir
        default_code_dir = os.path.join(os.path.dirname(__file__), "data", "code_examples")
        process_directory(default_code_dir, "code_example")
