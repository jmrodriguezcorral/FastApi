from pydantic import BaseModel

class User(BaseModel):
    id: str | None
    nombre_usuario: str
    correo: str