import os
import re
import glob
import logging
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("database")

class InMemoryCursor:
    def __init__(self, items):
        self._items = items

    def sort(self, key_or_list, direction=1):
        if isinstance(key_or_list, str):
            key = key_or_list
            rev = (direction == -1)
        elif isinstance(key_or_list, list) and key_or_list:
            key = key_or_list[0][0]
            rev = (key_or_list[0][1] == -1)
        else:
            return self

        def get_val(doc):
            val = doc.get(key)
            if val is None:
                return datetime.min if rev else datetime.max
            return val

        self._items = sorted(self._items, key=get_val, reverse=rev)
        return self

    def limit(self, n):
        self._items = self._items[:n]
        return self

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, index):
        return self._items[index]

class InMemoryCollection:
    def __init__(self, name):
        self.name = name
        self._docs = []

    def _match(self, doc, filter_dict):
        if not filter_dict:
            return True
        for k, v in filter_dict.items():
            if k.startswith("$"):
                continue
            doc_val = doc.get(k)
            if isinstance(v, dict):
                if "$ne" in v and doc_val == v["$ne"]:
                    return False
                if "$in" in v and doc_val not in v["$in"]:
                    return False
            elif isinstance(v, ObjectId):
                if str(doc_val) != str(v) and doc_val != v:
                    return False
            else:
                if str(doc_val) != str(v) and doc_val != v:
                    return False
        return True

    def find(self, filter_dict=None, projection=None):
        matched = [doc for doc in self._docs if self._match(doc, filter_dict)]
        return InMemoryCursor(matched)

    def find_one(self, filter_dict=None):
        for doc in self._docs:
            if self._match(doc, filter_dict):
                return doc
        return None

    def insert_one(self, doc):
        if "_id" not in doc or doc["_id"] is None:
            doc["_id"] = ObjectId()
        elif isinstance(doc["_id"], str):
            try:
                doc["_id"] = ObjectId(doc["_id"])
            except Exception:
                pass
        self._docs.append(doc)
        class InsertResult:
            def __init__(self, inserted_id):
                self.inserted_id = inserted_id
        return InsertResult(doc["_id"])

    def update_one(self, filter_dict, update_dict):
        doc = self.find_one(filter_dict)
        matched_count = 1 if doc else 0
        modified_count = 0
        if doc:
            self._apply_update(doc, update_dict)
            modified_count = 1
        class UpdateResult:
            def __init__(self, matched, modified):
                self.matched_count = matched
                self.modified_count = modified
        return UpdateResult(matched_count, modified_count)

    def find_one_and_update(self, filter_dict, update_dict, return_document=True):
        doc = self.find_one(filter_dict)
        if doc:
            self._apply_update(doc, update_dict)
            return doc
        return None

    def delete_one(self, filter_dict):
        doc = self.find_one(filter_dict)
        deleted_count = 0
        if doc in self._docs:
            self._docs.remove(doc)
            deleted_count = 1
        class DeleteResult:
            def __init__(self, cnt):
                self.deleted_count = cnt
        return DeleteResult(deleted_count)

    def count_documents(self, filter_dict=None):
        return len(list(self.find(filter_dict)))

    def create_index(self, *args, **kwargs):
        pass

    def _apply_update(self, doc, update_dict):
        if "$set" in update_dict:
            for k, v in update_dict["$set"].items():
                doc[k] = v
        if "$push" in update_dict:
            for k, v in update_dict["$push"].items():
                if k not in doc or not isinstance(doc[k], list):
                    doc[k] = []
                doc[k].append(v)

IS_DEMO_MODE = False
client = None
db = None

if not config.MONGODB_URI:
    logger.warning("MONGODB_URI não encontrada! Ativando Modo Demonstração (In-Memory Database).")
    IS_DEMO_MODE = True
else:
    try:
        client = MongoClient(config.MONGODB_URI, serverSelectionTimeoutMS=2500)
        client.admin.command('ping')
        try:
            db = client.get_database()
        except Exception:
            db = client["iara"]
        logger.info("MongoDB Atlas: Conexão estabelecida com sucesso!")
    except Exception as e:
        logger.warning(f"Erro ao conectar ao MongoDB Atlas ({e}). Ativando Modo Demonstração (In-Memory Database).")
        IS_DEMO_MODE = True

if IS_DEMO_MODE:
    users_collection = InMemoryCollection("users")
    chats_collection = InMemoryCollection("chats")
    document_chunks_collection = InMemoryCollection("document_chunks")
    code_examples_collection = InMemoryCollection("code_examples")
    classes_collection = InMemoryCollection("classes")
    exercise_catalog_collection = InMemoryCollection("exercise_catalog")
    concept_base_collection = InMemoryCollection("concept_base")

    # Seed default users
    import bcrypt
    def _hash(pw):
        return bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8')

    users_collection.insert_one({
        "name": "Administrador IARA",
        "email": "adm@iara.com",
        "password": _hash("iara123"),
        "role": "admin"
    })
    users_collection.insert_one({
        "name": "Prof. Carlos Silva",
        "email": "professor@iara.com",
        "password": _hash("iara123"),
        "role": "professor"
    })
    users_collection.insert_one({
        "name": "Aluno Exemplo",
        "email": "aluno@iara.com",
        "password": _hash("iara123"),
        "role": "aluno"
    })
    users_collection.insert_one({
        "name": "Aluno Exemplo EDU",
        "email": "aluno@iara.edu.br",
        "password": _hash("aluno123"),
        "role": "aluno"
    })

    # Seed default class
    default_class_id = ObjectId("66d000000000000000000001")
    classes_collection.insert_one({
        "_id": default_class_id,
        "name": "Algoritmos e Estruturas de Dados I",
        "code": "AED101",
        "description": "Turma de Introdução aos Algoritmos e Raciocínio Lógico de Programação.",
        "teacher_email": "professor@iara.com",
        "subject_type": "programming",
        "custom_guidelines": "Focar em raciocínio socrático e conceitos fundamentais de C++ / Python.",
        "rag_summary": "Conceitos de variáveis, operadores, laços de repetição (while, for), vetores e funções.",
        "created_at": datetime.utcnow()
    })

    # Seed default chat
    chats_collection.insert_one({
        "_id": ObjectId("66d000000000000000000002"),
        "userId": "aluno@iara.com",
        "title": "Dúvida sobre Laço While",
        "class_id": str(default_class_id),
        "class_name": "Algoritmos e Estruturas de Dados I",
        "messages": [
            {"role": "user", "content": "Como funciona o laço while em C++?"},
            {"role": "assistant", "content": "### 🧠 Laço de Repetição `while` em C++\n\nO laço `while` executa um bloco de código **enquanto** uma condição booleana for verdadeira.\n\n```cpp\nint i = 0;\nwhile (i < 5) {\n    cout << \"Iteração: \" << i << endl;\n    i++; // Incremento importante para evitar loop infinito!\n}\n```\n\n**Pontos Importantes:**\n1. A condição é avaliada **antes** de cada execução.\n2. Lembre-se sempre de atualizar a variável de controle para que a condição se torne falsa eventualmente.\n\n💬 **Pergunta para reflexão:** O que aconteceria se esquecêssemos a linha `i++`?"}
        ],
        "isDeleted": False,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow()
    })

    # Load local concept markdown files into concept_base_collection
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    concept_files = glob.glob(os.path.join(data_dir, "concept_base", "*.md"))
    for filepath in concept_files:
        filename = os.path.basename(filepath)
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            sections = content.split("## ")
            for sec in sections:
                if not sec.strip():
                    continue
                lines = sec.strip().split("\n")
                title = lines[0].strip()
                concept_base_collection.insert_one({
                    "filename": filename,
                    "title": title,
                    "location": f"Seção: {title}",
                    "content": "## " + sec.strip(),
                    "category": "Conceitos",
                    "class_id": str(default_class_id)
                })
        except Exception as e:
            logger.warning(f"Erro ao carregar arquivo de conceito {filename}: {e}")

else:
    users_collection = db["users"]
    chats_collection = db["chats"]
    document_chunks_collection = db["document_chunks"]
    code_examples_collection = db["code_examples"]
    classes_collection = db["classes"]
    exercise_catalog_collection = db["exercise_catalog"]
    concept_base_collection = db["concept_base"]

def check_connection():
    if IS_DEMO_MODE:
        return True
    try:
        client.admin.command('ping')
        logger.info("MongoDB Atlas: Conexão estabelecida com sucesso!")
        return True
    except Exception as e:
        logger.error(f"Erro ao conectar ao MongoDB Atlas: {e}")
        return False

