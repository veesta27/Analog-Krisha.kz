# backend/app/models/user.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from app.database import Base # Импортируем Base из шага 2

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False) # Пароль храним только в хэшированном виде!
    created_at = Column(DateTime, default=datetime.utcnow)

class Category(Base):
    __tablename__ = "Category"
    
    title = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    status = Column(Boolean, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    photo = Column(String, nullable=True)  # nullable=True, если фото необязательно