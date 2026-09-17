from fastapi import APIRouter, UploadFile, File, Form, Query, HTTPException, status
from typing import Optional
import os
import shutil
import tempfile
from database import document_chunks_collection, exercise_catalog_collection, concept_base_collection
from services.rag_service import ingest_document

router = APIRouter(prefix="/api/documents", tags=["documents"])

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    category: str = Form("concept"),
    class_id: Optional[str] = Form(None)
):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        count = ingest_document(filename=file.filename, file_path=tmp_path, category=category, class_id=class_id)
        os.remove(tmp_path)

        return {
            "message": f"Documento '{file.filename}' processado com sucesso!",
            "chunks_created": count,
            "category": category,
            "class_id": class_id
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar documento: {str(e)}")

@router.get("")
def list_documents(class_id: Optional[str] = Query(None)):
    pipeline = []
    if class_id:
        pipeline.append({"$match": {"class_id": class_id}})

    pipeline.extend([
        {
            "$group": {
                "_id": "$filename",
                "category": {"$first": "$category"},
                "chunks_count": {"$sum": 1}
            }
        },
        {"$sort": {"_id": 1}}
    ])

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
def delete_document(filename: str, class_id: Optional[str] = Query(None)):
    filter_query = {"filename": filename}
    if class_id:
        filter_query["class_id"] = class_id

    res1 = document_chunks_collection.delete_many(filter_query)
    res2 = exercise_catalog_collection.delete_many(filter_query)
    res3 = concept_base_collection.delete_many(filter_query)
    
    total_deleted = res1.deleted_count + res2.deleted_count + res3.deleted_count
    if total_deleted == 0:
        raise HTTPException(status_code=404, detail="Documento não encontrado.")

    if class_id:
        from services.rag_service import update_class_rag_summary
        update_class_rag_summary(class_id)

    return {"message": f"Documento '{filename}' e seus {total_deleted} chunks foram excluídos."}
