# backend/app/schemas/user.py
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr # Проверит, что это реальный email (с собачкой @)
    phone: str
    password: str

class Advertisements(BaseModel):
    title: str
    price: int
    room_num: int
    square: int
    city: str
    name: str
    date: datetime
    photo: str

class UserLoginStrict(BaseModel):
    email: EmailStr
    password: str
    phone: str