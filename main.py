from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from src import crud, models, schemas
from src.database import SessionLocal, engine

# Esto crea las tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Principal")

# Dependencia: Crea una sesión de base de datos por cada petición y la cierra al terminar
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def leer_raiz():
    return {"mensaje": "¡Base de datos anal...izada y servidor funcionando!"}

# --- NUEVOS ENDPOINTS ---

# 1. Crear un usuario (POST)
@app.post("/usuarios/", response_model=schemas.UsuarioResponse)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    # Verificamos si el correo ya existe
    db_usuario = crud.get_usuario_by_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    return crud.create_usuario(db=db, usuario=usuario)

# 2. Leer lista de usuarios (GET)
@app.get("/usuarios/", response_model=list[schemas.UsuarioResponse])
def leer_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    usuarios = crud.get_usuarios(db, skip=skip, limit=limit)
    return usuarios


# 3. Actualizar un usuario (PUT)
@app.put("/usuarios/{usuario_id}", response_model=schemas.UsuarioResponse)
def actualizar_usuario(usuario_id: int, usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = crud.update_usuario(db=db, usuario_id=usuario_id, nombre=usuario.nombre, email=usuario.email)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

# 4. Eliminar un usuario (DELETE)
@app.delete("/usuarios/{usuario_id}", response_model=schemas.UsuarioResponse)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = crud.delete_usuario(db=db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario
