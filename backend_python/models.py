from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    name: str
    email: str
    role: str = "user"

class MessageSchema(BaseModel):
    role: str # 'system', 'user', 'assistant'
    content: str

class CreateChatRequest(BaseModel):
    userId: str
    title: Optional[str] = "Nova Conversa"
    messages: Optional[List[MessageSchema]] = []

class UpdateChatRequest(BaseModel):
    title: Optional[str] = None
    message: Optional[MessageSchema] = None

class RenameChatRequest(BaseModel):
    title: str

class AddMessageRequest(BaseModel):
    message: MessageSchema

class DocumentChunkModel(BaseModel):
    filename: str
    chunk_index: int
    content: str
    embedding: List[float]
    category: str = "general" # 'concept' ou 'code_example'
    metadata: dict = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
