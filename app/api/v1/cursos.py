from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db import models
from app.schemas.curso import CursoIn
from app.schemas.curso_update import CursoUpdate
from fastapi import Path
from app.core.deps import get_current_user, require_role

router = APIRouter()

@router.get("")
def listar_cursos(db: Session = Depends(get_db)):
    cursos = db.query(models.Curso).all()
    return [{"id": c.id, "nombre": c.nombre, "descripcion": c.descripcion, "docente_id": c.docente_id} for c in cursos]

@router.post("", dependencies=[Depends(require_role("DOCENTE"))])
def crear_curso(data: CursoIn, user=Depends(get_current_user), db: Session = Depends(get_db)):
    curso = models.Curso(nombre=data.nombre, descripcion=data.descripcion, docente_id=user.id)
    db.add(curso)
    db.commit()
    db.refresh(curso)
    return {"id": curso.id, "nombre": curso.nombre, "descripcion": curso.descripcion, "docente_id": curso.docente_id}


# Editar curso
@router.put("/{curso_id}", dependencies=[Depends(require_role("DOCENTE"))])
def editar_curso(
    curso_id: int = Path(...),
    data: CursoUpdate = None,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    curso = db.query(models.Curso).filter_by(id=curso_id, docente_id=user.id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    if data.nombre is not None:
        curso.nombre = data.nombre
    if data.descripcion is not None:
        curso.descripcion = data.descripcion
    db.commit()
    db.refresh(curso)
    return {"id": curso.id, "nombre": curso.nombre, "descripcion": curso.descripcion, "docente_id": curso.docente_id}

# Eliminar curso
@router.delete("/{curso_id}", dependencies=[Depends(require_role("DOCENTE"))])
def eliminar_curso(
    curso_id: int = Path(...),
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    curso = db.query(models.Curso).filter_by(id=curso_id, docente_id=user.id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    db.delete(curso)
    db.commit()
    return {"ok": True}
