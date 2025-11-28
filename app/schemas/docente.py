from pydantic import BaseModel
from typing import Optional

class DocenteUpdateImage(BaseModel):
    imagen: Optional[str]  # URL o ruta de la imagen

class DocenteOut(BaseModel):
    id: int
    nombre: str
    email: str
    rol: str
    imagen: Optional[str]

    class Config:
        orm_mode = True
