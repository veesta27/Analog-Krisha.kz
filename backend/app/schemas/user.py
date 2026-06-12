# backend/app/schemas/user.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr # Проверит, что это реальный email (с собачкой @)
    phone: str
    password: str