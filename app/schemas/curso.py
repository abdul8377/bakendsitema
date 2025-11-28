from pydantic import BaseModel
from typing import Optional

class CursoIn(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class CursoOut(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    docente_id: int
