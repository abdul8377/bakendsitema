from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db import models
from app.schemas.auth import RegisterIn, LoginIn, AuthOut
from app.core.security import get_password_hash, verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=dict, status_code=201)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    exists = db.query(models.Usuario).filter_by(email=payload.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    user = models.Usuario(
        nombre=payload.nombre,
        email=payload.email,
        password_hash=get_password_hash(payload.password),
        rol=payload.rol.upper()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "nombre": user.nombre, "email": user.email, "rol": user.rol}

@router.post("/login", response_model=AuthOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(models.Usuario).filter_by(email=payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    token = create_access_token({"sub": str(user.id), "rol": user.rol})
    return {"access_token": token, "user": {"id": user.id, "nombre": user.nombre, "rol": user.rol}}
