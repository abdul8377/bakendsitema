from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db import models
from app.core.deps import get_current_user, require_role

router = APIRouter()

@router.get("/mis-notas", dependencies=[Depends(require_role("ESTUDIANTE"))])
def mis_notas(user=Depends(get_current_user), db: Session = Depends(get_db)):
    notas = db.query(models.Nota).filter_by(estudiante_id=user.id).all()
    return [{"id": n.id, "curso_id": n.curso_id, "nota": n.nota, "actualizado_en": str(n.actualizado_en)} for n in notas]

@router.post("", dependencies=[Depends(require_role("DOCENTE"))])
def crear_nota(payload: dict, user=Depends(get_current_user), db: Session = Depends(get_db)):
    # validar que el docente es dueño del curso
    curso_id = payload.get("curso_id")
    estudiante_id = payload.get("estudiante_id")
    nota_val = float(payload.get("nota"))
    curso = db.get(models.Curso, curso_id)
    if not curso or curso.docente_id != user.id:
        raise HTTPException(status_code=403, detail="No autorizado para calificar este curso")
    
    # Buscar si ya existe nota
    nota_existente = db.query(models.Nota).filter(models.Nota.curso_id == curso_id, models.Nota.estudiante_id == estudiante_id).first()
    
    if nota_existente:
        nota_existente.nota = nota_val
        db.commit()
        db.refresh(nota_existente)
        return {"id": nota_existente.id, "curso_id": nota_existente.curso_id, "nota": nota_existente.nota}
    
    nota = models.Nota(estudiante_id=estudiante_id, curso_id=curso_id, nota=nota_val)
    db.add(nota)
    db.commit()
    db.refresh(nota)
    return {"id": nota.id, "curso_id": nota.curso_id, "nota": nota.nota}

@router.put("/{curso_id}/{estudiante_id}", dependencies=[Depends(require_role("DOCENTE"))])
def actualizar_nota(
    curso_id: int, 
    estudiante_id: int, 
    payload: dict, 
    user=Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    # Validar que el docente es dueño del curso
    curso = db.query(models.Curso).filter(models.Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    if curso.docente_id != user.id:
        raise HTTPException(status_code=403, detail="No autorizado")

    nota_val = float(payload.get("nota"))
    
    # Buscar nota existente
    nota = db.query(models.Nota).filter(models.Nota.curso_id == curso_id, models.Nota.estudiante_id == estudiante_id).first()
    
    if nota:
        nota.nota = nota_val
    else:
        nota = models.Nota(estudiante_id=estudiante_id, curso_id=curso_id, nota=nota_val)
        db.add(nota)
    
    db.commit()
    db.refresh(nota)
    return {"ok": True, "nota": nota.nota}
