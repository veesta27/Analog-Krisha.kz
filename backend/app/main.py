# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.models import user # Твой импорт моделей
from app.schemas.user import UserCreate # Импорт схемы из Шага 2
from passlib.context import CryptContext

# Создаем таблицы при старте
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Krisha Analog API")

# Настройка шифрования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.get("/")
def home():
    return {"status": "Бэкенд работает, база данных успешно подключена!"}

# --- ДОБАВЛЯЕМ ЭНДПОИНТ РЕГИСТРАЦИИ ---
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

    # 3. Хэшируем пароль
    hashed_pwd = pwd_context.hash(user_data.password)

    # 4. Создаем запись
    new_user = user.User(
        name=user_data.name,
        email=user_data.email,
        phone=user_data.phone,
        hashed_password=hashed_pwd
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"status": "success", "message": "Пользователь успешно создан!", "user_id": new_user.id}