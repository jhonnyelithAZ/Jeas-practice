from fastapi import FastAPI
from src import models
from src.database import engine

# Esta línea crea el archivo de la base de datos y las tablas definidas en models.py
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mi Primera API")

@app.get("/")
def leer_raiz():
    return {"mensaje": "¡Hola, mundo! El servidor FastAPI está funcionando."}