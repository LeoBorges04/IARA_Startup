from fastapi import APIRouter, HTTPException, status
from models import UserRegister, UserLogin, UserResponse
from services.auth_service import register_user, authenticate_user

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister):
    user_res, error = register_user(user_data)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {
        "message": "Cadastro realizado com sucesso!",
        "user": user_res
    }

@router.post("/login")
def login(login_data: UserLogin):
    user_res, error = authenticate_user(login_data)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return user_res
