from pydantic import BaseModel

# Esquema para cuando creamos un usuario (no pedimos ID ni si está activo)
class UsuarioCreate(BaseModel):
    nombre: str
    email: str

# Esquema para cuando devolvemos un usuario (incluye ID y estado)
class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    email: str
    activo: bool

    class Config:
        from_attributes = True