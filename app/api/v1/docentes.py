from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db import models
from app.core.deps import get_current_user, require_role
import os
from app.schemas.docente import DocenteOut

router = APIRouter()

# Carpeta donde se guardarán las imágenes
UPLOAD_FOLDER = "uploaded_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.get("/docente/dashboard", dependencies=[Depends(require_role("DOCENTE"))])
def dashboard_docente(user=Depends(get_current_user), db: Session = Depends(get_db)):
    cursos = db.query(models.Curso).filter_by(docente_id=user.id).all()
    return {
        "id": user.id,
        "nombre": user.nombre,
        "email": user.email,
        "imagen": user.imagen,
        "cursos": [{"id": c.id, "nombre": c.nombre} for c in cursos],
        "total_cursos": len(cursos)
    }


# Endpoint para subir imagen de docente
@router.post("/docente/upload-image", response_model=DocenteOut, dependencies=[Depends(require_role("DOCENTE"))])
def upload_docente_image(
    file: UploadFile = File(...),
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validar tipo de archivo
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")
    # Guardar archivo
    filename = f"docente_{user.id}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(file_path, "wb") as image_file:
        image_file.write(file.file.read())
    # Actualizar usuario
    user.imagen = file_path
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
