
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db import models
from app.core.deps import get_current_user, require_role

router = APIRouter()

@router.delete("/cursos/{curso_id}/desinscribir", dependencies=[Depends(require_role("ESTUDIANTE"))])
def desinscribir(curso_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    ins = db.query(models.Inscripcion).filter_by(estudiante_id=user.id, curso_id=curso_id).first()
    if not ins:
        raise HTTPException(status_code=404, detail="No estás inscrito en este curso")
    db.delete(ins)
    db.commit()
    return {"ok": True, "curso_id": curso_id}

@router.get("/mis-cursos", dependencies=[Depends(require_role("ESTUDIANTE"))])
def mis_cursos(user=Depends(get_current_user), db: Session = Depends(get_db)):
    # Simple: retorna inscripciones por curso (si existieran)
    ins = db.query(models.Inscripcion).filter_by(estudiante_id=user.id).all()
    return [{"curso_id": i.curso_id, "fecha_inscripcion": str(i.fecha_inscripcion)} for i in ins]

@router.post("/cursos/{curso_id}/inscribir", dependencies=[Depends(require_role("ESTUDIANTE"))])
def inscribir(curso_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    curso = db.get(models.Curso, curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    # evitar duplicados
    exists = db.query(models.Inscripcion).filter_by(estudiante_id=user.id, curso_id=curso_id).first()
    if exists:
        return {"ok": True, "message": "Ya estás inscrito"}
    ins = models.Inscripcion(estudiante_id=user.id, curso_id=curso_id)
    db.add(ins)
    db.commit()
    return {"ok": True, "curso_id": curso_id}
