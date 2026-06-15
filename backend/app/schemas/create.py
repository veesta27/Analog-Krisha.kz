# backend/app/schemas/user.py
from pydantic import BaseModel, EmailStr, ConfigDict, computed_field
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr # Проверит, что это реальный email (с собачкой @)
    phone: str
    password: str

class UserLoginStrict(BaseModel):
    email: EmailStr
    password: str
    phone: str

# Схема для создания
class AdvertisementCreate(BaseModel):
    title: str
    description: str  
    price: int
    status: bool = True
    room_num: int
    square: int
    city: str
    name: str
    photo: Optional[str] = None

# Схема для ответа
class AdvertisementsResponse(BaseModel):
    id: int
    title: str
    description: str  
    price: int
    status: bool 
    room_num: int
    square: int
    city: str
    name: str
    photo: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def status_text(self) -> str:
        return "в наличии" if self.status else "нет в наличии"