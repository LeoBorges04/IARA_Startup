from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from typing import Optional, List
from database import chats_collection
from models import CreateChatRequest, UpdateChatRequest, RenameChatRequest, AddMessageRequest, MessageSchema
from services.rag_service import generate_chat_response, generate_chat_title
from datetime import datetime

router = APIRouter(prefix="/api/chats", tags=["chats"])

def format_chat(chat_doc):
    if not chat_doc:
        return None
    chat_doc["_id"] = str(chat_doc["_id"])
    return chat_doc

@router.get("/{user_id}")
def get_user_chats(user_id: str):
    try:
        chats = list(chats_collection.find({"userId": user_id, "isDeleted": {"$ne": True}}).sort("updatedAt", -1))
        return [format_chat(c) for c in chats]
    except Exception as e:
        print(f"Erro ao buscar conversas do usuário no MongoDB: {e}")
        return []

@router.post("", status_code=status.HTTP_201_CREATED)
def create_chat(chat_data: CreateChatRequest):
    now = datetime.utcnow()
    new_chat = {
        "userId": chat_data.userId,
        "title": chat_data.title or "Nova Conversa",
        "messages": [m.dict() for m in chat_data.messages] if chat_data.messages else [],
        "isDeleted": False,
        "createdAt": now,
        "updatedAt": now
    }
    result = chats_collection.insert_one(new_chat)
    new_chat["_id"] = str(result.inserted_id)
    return new_chat

@router.put("/{chat_id}")
def update_chat(chat_id: str, payload: UpdateChatRequest):
    try:
        obj_id = ObjectId(chat_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de conversa inválido.")

    update_doc = {"$set": {"updatedAt": datetime.utcnow()}}
    if payload.title:
        update_doc["$set"]["title"] = payload.title
    if payload.message:
        update_doc["$push"] = {"messages": payload.message.dict()}

    updated = chats_collection.find_one_and_update(
        {"_id": obj_id},
        update_doc,
        return_document=True
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Conversa não encontrada.")
    return format_chat(updated)

@router.delete("/{chat_id}")
def delete_chat(chat_id: str):
    try:
        obj_id = ObjectId(chat_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de conversa inválido.")

    result = chats_collection.update_one({"_id": obj_id}, {"$set": {"isDeleted": True}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Conversa não encontrada.")
    return {"message": "Conversa excluída com sucesso."}

@router.put("/{chat_id}/rename")
def rename_chat(chat_id: str, payload: RenameChatRequest):
    try:
        obj_id = ObjectId(chat_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de conversa inválido.")

    updated = chats_collection.find_one_and_update(
        {"_id": obj_id},
        {"$set": {"title": payload.title, "updatedAt": datetime.utcnow()}},
        return_document=True
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Conversa não encontrada.")
    return format_chat(updated)

@router.post("/{chat_id}/message")
def process_message(chat_id: str, payload: AddMessageRequest):
    try:
        obj_id = ObjectId(chat_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de conversa inválido.")

    user_msg_dict = payload.message.dict()
    chat = chats_collection.find_one_and_update(
        {"_id": obj_id},
        {
            "$push": {"messages": user_msg_dict},
            "$set": {"updatedAt": datetime.utcnow()}
        },
        return_document=True
    )
    if not chat:
        raise HTTPException(status_code=404, detail="Conversa não encontrada.")

    bot_reply_content = generate_chat_response(chat.get("messages", []), payload.message.content)
    bot_msg_obj = {"role": "assistant", "content": bot_reply_content}

    chats_collection.update_one(
        {"_id": obj_id},
        {"$push": {"messages": bot_msg_obj}}
    )

    new_title = None
    user_messages = [m for m in chat.get("messages", []) if m.get("role") == "user"]
    if len(user_messages) == 1 and chat.get("title") == "Nova Conversa":
        generated_title = generate_chat_title(payload.message.content)
        if generated_title:
            chats_collection.update_one({"_id": obj_id}, {"$set": {"title": generated_title}})
            new_title = generated_title

    return {
        "botMsgObj": bot_msg_obj,
        "newTitle": new_title
    }
