from sqlalchemy.orm import Session
from src import models, schemas

# Función para leer un usuario por su ID
def get_usuario(db: Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

# Función para leer un usuario por su email
def get_usuario_by_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

# Función para leer todos los usuarios (con límite de paginación opcional)
def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Usuario).offset(skip).limit(limit).all()

# Función para crear un nuevo usuario en la base de datos
def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    # 1. Crear la instancia del modelo de SQLAlchemy
    db_usuario = models.Usuario(nombre=usuario.nombre, email=usuario.email)
    
    # 2. Añadirlo a la sesión de la base de datos
    db.add(db_usuario)
    
    # 3. Confirmar los cambios (guardar en la tabla)
    db.commit()
    
    # 4. Refrescar la instancia para obtener el ID generado automáticamente
    db.refresh(db_usuario)
    
    return db_usuario

# Función para actualizar los datos de un usuario
def update_usuario(db: Session, usuario_id: int, nombre: str, email: str):
    # 1. Buscamos si el usuario existe
    db_usuario = get_usuario(db, usuario_id=usuario_id)
    
    if db_usuario:
        # 2. Actualizamos sus datos
        db_usuario.nombre = nombre
        db_usuario.email = email
        # 3. Guardamos los cambios
        db.commit()
        db.refresh(db_usuario)
        
    return db_usuario

# Función para eliminar un usuario
def delete_usuario(db: Session, usuario_id: int):
    # 1. Buscamos al usuario
    db_usuario = get_usuario(db, usuario_id=usuario_id)
    
    if db_usuario:
        # 2. Lo eliminamos de la sesión
        db.delete(db_usuario)
        # 3. Confirmamos la eliminación
        db.commit()
        
    return db_usuario