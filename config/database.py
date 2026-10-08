"""
Configuración de la base de datos SQLite
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Directorio compartido para la app local
DB_DIR = os.path.join(os.path.expanduser("~"), "SHIFTMODE_DATA")
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

DATABASE_URL = f"sqlite:///{os.path.join(DB_DIR, 'shiftmode.db')}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)


def get_session():
    return SessionLocal()
