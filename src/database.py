from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexión a Postgres (coincide con los datos del docker-compose)
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://admin:adminpassword@localhost:5433/fastapi_db"

# Engine para Postgres (eliminamos el connect_args exclusivo de SQLite)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()