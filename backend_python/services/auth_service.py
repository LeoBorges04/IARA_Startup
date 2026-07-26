import bcrypt
import logging
from database import users_collection
from models import UserRegister, UserLogin

logger = logging.getLogger("auth_service")

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(10)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        logger.error(f"Erro ao verificar senha: {e}")
        return False

def register_user(user_data: UserRegister):
    existing = users_collection.find_one({"email": user_data.email})
    if existing:
        return None, "Este e-mail já está cadastrado."

    hashed = hash_password(user_data.password)
    user_doc = {
        "name": user_data.name,
        "email": user_data.email,
        "password": hashed,
        "role": "user"
    }
    
    users_collection.insert_one(user_doc)
    return {
        "name": user_doc["name"],
        "email": user_doc["email"],
        "role": user_doc["role"]
    }, None

def authenticate_user(login_data: UserLogin):
    user = users_collection.find_one({"email": login_data.email})
    if not user:
        return None, "E-mail ou senha inválidos."

    if not verify_password(login_data.password, user["password"]):
        return None, "E-mail ou senha inválidos."

    return {
        "name": user["name"],
        "email": user["email"],
        "role": user.get("role", "user")
    }, None

def seed_admin_user():
    """Garante que a conta de admin inicial exista (adm@iara.com / iara123)."""
    admin_email = "adm@iara.com"
    existing = users_collection.find_one({"email": admin_email})
    if not existing:
        hashed = hash_password("iara123")
        users_collection.insert_one({
            "name": "Administradores",
            "email": admin_email,
            "password": hashed,
            "role": "admin"
        })
        logger.info("Conta de administrador criada com sucesso (adm@iara.com)!")
