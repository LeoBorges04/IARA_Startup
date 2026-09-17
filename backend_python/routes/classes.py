from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from typing import List, Optional
from datetime import datetime
from database import classes_collection
from models import CreateClassRequest, UpdateClassGuidelinesRequest, ClassResponse

router = APIRouter(prefix="/api/classes", tags=["classes"])

def format_class(class_doc):
    if not class_doc:
        return None
    c_id = str(class_doc["_id"])
    return {
        "id": c_id,
        "_id": c_id,
        "name": class_doc.get("name", ""),
        "code": class_doc.get("code", ""),
        "description": class_doc.get("description", ""),
        "teacher_email": class_doc.get("teacher_email", ""),
        "subject_type": class_doc.get("subject_type", "programming"),
        "custom_guidelines": class_doc.get("custom_guidelines", ""),
        "rag_summary": class_doc.get("rag_summary", ""),
        "created_at": class_doc.get("created_at", datetime.utcnow())
    }

@router.post("", status_code=status.HTTP_201_CREATED)
def create_class(payload: CreateClassRequest):
    existing = classes_collection.find_one({
        "teacher_email": payload.teacher_email,
        "code": payload.code.strip().upper()
    })
    if existing:
        raise HTTPException(status_code=400, detail=f"Você já possui uma turma cadastrada com o código '{payload.code}'.")

    now = datetime.utcnow()
    new_class = {
        "name": payload.name.strip(),
        "code": payload.code.strip().upper(),
        "description": payload.description.strip() if payload.description else "",
        "teacher_email": payload.teacher_email.strip(),
        "subject_type": payload.subject_type if payload.subject_type in ["programming", "custom"] else "programming",
        "custom_guidelines": payload.custom_guidelines.strip() if payload.custom_guidelines else "",
        "created_at": now
    }
    result = classes_collection.insert_one(new_class)
    new_class["_id"] = result.inserted_id
    return format_class(new_class)

@router.get("")
def list_all_classes():
    """Retorna todas as turmas ativas no sistema para a seleção dos alunos."""
    try:
        classes = list(classes_collection.find({}).sort("created_at", -1))
        return [format_class(c) for c in classes]
    except Exception as e:
        print(f"Erro ao listar turmas: {e}")
        return []

@router.get("/teacher/{email}")
def get_teacher_classes(email: str):
    """Retorna a lista de turmas pertencentes a um professor específico."""
    try:
        classes = list(classes_collection.find({"teacher_email": email.strip()}).sort("created_at", -1))
        return [format_class(c) for c in classes]
    except Exception as e:
        print(f"Erro ao buscar turmas do professor: {e}")
        return []

@router.get("/{class_id}")
def get_class_by_id(class_id: str):
    try:
        obj_id = ObjectId(class_id)
        class_doc = classes_collection.find_one({"_id": obj_id})
        if not class_doc:
            raise HTTPException(status_code=404, detail="Turma não encontrada.")
        return format_class(class_doc)
    except Exception as e:
        raise HTTPException(status_code=400, detail="ID de turma inválido.")

@router.put("/{class_id}/guidelines")
def update_class_guidelines(class_id: str, payload: UpdateClassGuidelinesRequest):
    try:
        obj_id = ObjectId(class_id)
        updated = classes_collection.find_one_and_update(
            {"_id": obj_id},
            {"$set": {"custom_guidelines": payload.custom_guidelines.strip()}},
            return_document=True
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Turma não encontrada.")
        return format_class(updated)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar diretrizes: {str(e)}")

@router.delete("/{class_id}")
def delete_class(class_id: str):
    try:
        obj_id = ObjectId(class_id)
        res = classes_collection.delete_one({"_id": obj_id})
        if res.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Turma não encontrada.")
        return {"message": "Turma excluída com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao excluir turma: {str(e)}")
