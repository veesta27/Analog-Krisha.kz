# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.models import user
from app.schemas.create import UserCreate, UserLoginStrict, AdvertisementCreate, AdvertisementsResponse
from fastapi.middleware.cors import CORSMiddleware
import bcrypt # <- ИМПОРТИРУЕМ НАПРЯМУЮ BCRYPT ВМЕСТО PASSLIB

# Создаем таблицы при старте
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Krisha Analog API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешает запросы откуда угодно (для MVP это нормально)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешает любые методы (POST, GET и т.д.)
    allow_headers=["*"],  # Разрешает любые заголовки
)

@app.get("/")
def home():
    return {"status": "Бэкенд работает, база данных успешно подключена!"}

# API URL
@app.post("/api/register", status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # 1. Проверяем уникальность email
    db_user = db.query(user.User).filter(user.User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Пользователь с такой почтой уже зарегистрирован")

    # 2. Проверяем уникальность телефона
    db_phone = db.query(user.User).filter(user.User.phone == user_data.phone).first()
    if db_phone:
        raise HTTPException(status_code=400, detail="Пользователь с таким телефоном уже зарегистрирован")

    # 3. ХЭШИРУЕМ ПАРОЛЬ НАПРЯМУЮ ЧЕРЕЗ BCRYPT
    # Переводим пароль в байты
    password_bytes = user_data.password.encode('utf-8')
    # Генерируем соль
    salt = bcrypt.gensalt()
    # Хэшируем и переводим обратно в строку для хранения в БД
    hashed_pwd = bcrypt.hashpw(password_bytes, salt).decode('utf-8')

    # 4. Создаем запись
    new_user = user.User(
        name=user_data.username,
        email=user_data.email,
        phone=user_data.phone,
        hashed_password=hashed_pwd # Сохраняем наш чистый хэш
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"status": "success", "message": "Пользователь успешно создан!", "user_id": new_user.id}

@app.post("/api/login")
def login_user(login_data: UserLoginStrict, db: Session = Depends(get_db)):
    # 1. Ищем пользователя, у которого совпадает И email, И телефон
    db_user = db.query(user.User).filter(
        user.User.email == login_data.email,
        user.User.phone == login_data.phone
    ).first()
    
    # Если юзер не найден (не совпала почта или телефон)
    if not db_user:
        raise HTTPException(status_code=400, detail="Неверные данные для входа")

    # 2. ПРОВЕРЯЕМ ПАРОЛЬ ЧЕРЕЗ BCRYPT
    # Переводим введенный юзером пароль в байты
    provided_password_bytes = login_data.password.encode('utf-8')
    # Достаем захэшированный пароль из БД и тоже переводим в байты
    stored_hash_bytes = db_user.hashed_password.encode('utf-8')

    # Сверяем хэши
    is_valid_password = bcrypt.checkpw(provided_password_bytes, stored_hash_bytes)

    if not is_valid_password:
        raise HTTPException(status_code=400, detail="Неверные данные для входа")

    # 3. Успешный вход
    return {
        "status": "success", 
        "message": "Вы успешно вошли!", 
        "user_id": db_user.id
    }  

@app.post("/api/add", response_model=AdvertisementsResponse, status_code=status.HTTP_201_CREATED)
def create_advertisement(ad_data: AdvertisementCreate, db: Session = Depends(get_db)):
    
    # 1. Распаковываем входные данные в модель БД
    new_ad = user.Add(**ad_data.model_dump())

    # 2. Сохраняем в базу
    db.add(new_ad)
    db.commit()
    db.refresh(new_ad) # Получаем ID из базы

    # 3. Возвращаем просто объект базы данных.
    # FastAPI сам превратит его в AdvertisementsResponse, 
    # потому что мы указали это в декораторе @app.post!
    return new_ad

from typing import List # Если у тебя старая версия Python, но обычно работает просто list[]

@app.get("/api/ads", response_model=list[AdvertisementsResponse])
def get_all_ads(db: Session = Depends(get_db)):
    
    # 1. Делаем запрос к базе данных: "Достань мне ВСЕ записи из таблицы Add"
    ads = db.query(user.Add).all()
    
    # 2. Просто возвращаем этот список
    # FastAPI сам пробежится по каждому объявлению и пропустит его 
    # через AdvertisementsResponse (добавив status_text)
    return ads