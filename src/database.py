from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Cuando levantes tu contenedor de Postgres, cambiaremos esta URL por:
# SQLALCHEMY_DATABASE_URL = "postgresql://usuario:password@localhost:5432/mi_base"
SQLALCHEMY_DATABASE_URL = "sqlite:///./mi_app.db"

# connect_args={"check_same_thread": False} es una configuración exclusiva de SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()