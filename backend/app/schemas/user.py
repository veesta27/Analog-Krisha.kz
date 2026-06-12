# backend/app/schemas/user.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr # Проверит, что это реальный email (с собачкой @)
    phone: str
    password: str