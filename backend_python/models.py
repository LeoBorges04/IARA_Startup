from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = "aluno"

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
    class_id: Optional[str] = None
    class_name: Optional[str] = None

class CreateClassRequest(BaseModel):
    name: str
    code: str
    description: Optional[str] = ""
    teacher_email: EmailStr
    subject_type: str = "programming" # 'programming' ou 'custom'
    custom_guidelines: Optional[str] = ""

class UpdateClassGuidelinesRequest(BaseModel):
    custom_guidelines: str

class ClassResponse(BaseModel):
    id: str
    name: str
    code: str
    description: Optional[str] = ""
    teacher_email: str
    subject_type: str = "programming"
    custom_guidelines: Optional[str] = ""
    created_at: datetime

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
    class_id: Optional[str] = None
    metadata: dict = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
