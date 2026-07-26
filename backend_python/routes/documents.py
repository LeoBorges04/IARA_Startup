from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
import os
import shutil
import tempfile
from database import document_chunks_collection, exercise_catalog_collection, concept_base_collection

router = APIRouter(prefix="/api/documents", tags=["documents"])

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    category: str = Form("concept")
):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        count = ingest_document(filename=file.filename, file_path=tmp_path, category=category)
        os.remove(tmp_path)

        return {
            "message": f"Documento '{file.filename}' processado com sucesso!",
            "chunks_created": count,
            "category": category
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar documento: {str(e)}")

@router.get("")
def list_documents():
    pipeline = [
        {
            "$group": {
                "_id": "$filename",
                "category": {"$first": "$category"},
                "chunks_count": {"$sum": 1}
            }
        },
        {"$sort": {"_id": 1}}
    ]
    docs_chunks = list(document_chunks_collection.aggregate(pipeline))
    docs_ex = list(exercise_catalog_collection.aggregate(pipeline))
    docs_concept = list(concept_base_collection.aggregate(pipeline))
    
    all_map = {}
    for d in docs_chunks + docs_ex + docs_concept:
        fn = d["_id"]
        if fn not in all_map:
            all_map[fn] = {"filename": fn, "category": d.get("category", "concept"), "chunks_count": d["chunks_count"]}
            
    return sorted(list(all_map.values()), key=lambda x: x["filename"])

@router.delete("/{filename}")
def delete_document(filename: str):
    res1 = document_chunks_collection.delete_many({"filename": filename})
    res2 = exercise_catalog_collection.delete_many({"filename": filename})
    res3 = concept_base_collection.delete_many({"filename": filename})
    
    total_deleted = res1.deleted_count + res2.deleted_count + res3.deleted_count
    if total_deleted == 0:
        raise HTTPException(status_code=404, detail="Documento não encontrado.")
    return {"message": f"Documento '{filename}' e seus {total_deleted} chunks foram excluídos."}
