from pydantic import BaseModel
# Metemos este tipo por compatibilidad con python 3.9 con nueva version |None
from typing import Optional

class User(BaseModel):
    id: Optional[str]
    nombre_usuario: str
    correo: str