from fastapi import APIRouter
from database import users_collection, chats_collection

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.get("/users-chats")
def get_users_chats():
    users = list(users_collection.find({}, {"password": 0}))
    all_chats = list(chats_collection.find({}))

    chats_by_user = {}
    for chat in all_chats:
        chat["_id"] = str(chat["_id"])
        user_id = chat.get("userId")
        if user_id:
            if user_id not in chats_by_user:
                chats_by_user[user_id] = []
            chats_by_user[user_id].append(chat)

    enriched_users = []
    for user in users:
        user["_id"] = str(user["_id"])
        user["chats"] = chats_by_user.get(user["email"], [])
        enriched_users.append(user)

    return enriched_users
