import sys
import os
from datetime import datetime

# Adicionar caminho do backend ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database import users_collection, classes_collection, document_chunks_collection, concept_base_collection, exercise_catalog_collection
from services.auth_service import hash_password

MASTER_TEACHER_EMAIL = "prof.master@iara.edu.br"
MASTER_TEACHER_PASS = "ProfMasterIARA2026!"
MASTER_TEACHER_NAME = "Prof. Master IARA"
MASTER_CLASS_CODE = "MASTER-CPP-2026"
MASTER_CLASS_NAME = "Turma Principal - C++ & Algoritmos"

def run_migration():
    print("=" * 70)
    print("🚀 INICIANDO MIGRAÇÃO E REESTRUTURAÇÃO MULTITURMAS IARA")
    print("=" * 70)

    # 1. Criar ou Atualizar a conta do Professor Master
    hashed_pass = hash_password(MASTER_TEACHER_PASS)
    master_user = users_collection.find_one({"email": MASTER_TEACHER_EMAIL})
    if not master_user:
        res = users_collection.insert_one({
            "name": MASTER_TEACHER_NAME,
            "email": MASTER_TEACHER_EMAIL,
            "password": hashed_pass,
            "role": "professor",
            "created_at": datetime.utcnow()
        })
        master_user_id = str(res.inserted_id)
        print(f"✅ Conta do Professor Master criada com sucesso: {MASTER_TEACHER_EMAIL}")
    else:
        users_collection.update_one(
            {"email": MASTER_TEACHER_EMAIL},
            {"$set": {"password": hashed_pass, "role": "professor", "name": MASTER_TEACHER_NAME}}
        )
        master_user_id = str(master_user["_id"])
        print(f"✅ Conta do Professor Master atualizada: {MASTER_TEACHER_EMAIL}")

    # 2. Criar ou Atualizar a Turma Padrão Master
    master_class = classes_collection.find_one({"code": MASTER_CLASS_CODE})
    if not master_class:
        res_class = classes_collection.insert_one({
            "name": MASTER_CLASS_NAME,
            "code": MASTER_CLASS_CODE,
            "description": "Turma padrão migrada com todo o acervo didático de C++ e algoritmos.",
            "teacher_email": MASTER_TEACHER_EMAIL,
            "subject_type": "programming",
            "custom_guidelines": "",
            "created_at": datetime.utcnow()
        })
        master_class_id = str(res_class.inserted_id)
        print(f"✅ Turma Master criada com sucesso (ID: {master_class_id})")
    else:
        master_class_id = str(master_class["_id"])
        classes_collection.update_one(
            {"_id": master_class["_id"]},
            {"$set": {"subject_type": "programming", "teacher_email": MASTER_TEACHER_EMAIL}}
        )
        print(f"✅ Turma Master encontrada (ID: {master_class_id})")

    # 3. Migrar todo o acervo de RAG existente para a Turma Master
    up_chunks = document_chunks_collection.update_many(
        {"$or": [{"class_id": {"$exists": False}}, {"class_id": None}, {"class_id": ""}]},
        {"$set": {"class_id": master_class_id}}
    )
    up_concepts = concept_base_collection.update_many(
        {"$or": [{"class_id": {"$exists": False}}, {"class_id": None}, {"class_id": ""}]},
        {"$set": {"class_id": master_class_id}}
    )
    up_exercises = exercise_catalog_collection.update_many(
        {"$or": [{"class_id": {"$exists": False}}, {"class_id": None}, {"class_id": ""}]},
        {"$set": {"class_id": master_class_id}}
    )

    print(f"📦 Chunks de Documentos migrados para a Turma Master: {up_chunks.modified_count}")
    print(f"📘 Base Conceitual migrada para a Turma Master: {up_concepts.modified_count}")
    print(f"💻 Catálogo de Exercícios migrado para a Turma Master: {up_exercises.modified_count}")

    # 4. Limpar todas as outras contas de professores/admins registradas
    del_res = users_collection.delete_many({
        "role": {"$in": ["professor", "admin"]},
        "email": {"$ne": MASTER_TEACHER_EMAIL}
    })
    print(f"🧹 Contas de professores/admins antigas excluídas: {del_res.deleted_count}")

    print("=" * 70)
    print("🎉 MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
    print(f"👤 Credenciais do Professor Master:")
    print(f"   - Email: {MASTER_TEACHER_EMAIL}")
    print(f"   - Senha: {MASTER_TEACHER_PASS}")
    print("=" * 70)

if __name__ == "__main__":
    run_migration()
