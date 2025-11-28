from pydantic import BaseModel
from typing import Optional

class CursoIn(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class CursoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
