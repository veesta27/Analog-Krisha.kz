# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Указываем путь к файлу базы данных в корне папки backend
SQLALCHEMY_DATABASE_URL = "sqlite:///./krisha_base.db"

# 2. Создаем движок. 
# Аргумент check_same_thread нужен только для SQLite, чтобы разные запросы не блокировали друг друга
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Создаем сессию для работы с БД (через нее будем делать запросы)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Базовый класс, от которого мы будем наследовать все наши модели (User, Ad и т.д.)
Base = declarative_base()

# Функция для получения доступа к базе (пригодится в контроллерах)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()