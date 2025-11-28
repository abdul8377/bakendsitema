
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from fastapi.staticfiles import StaticFiles
import os
from app.api.v1.auth import router as auth_router
from app.api.v1.cursos import router as cursos_router
from app.api.v1.notas import router as notas_router
from app.api.v1.estudiantes import router as estudiantes_router
from app.api.v1.docentes import router as docentes_router
# Agregar imports para crear tablas
from app.db.base import Base
from app.db.session import engine



# Crear todas las tablas al iniciar la app
Base.metadata.create_all(bind=engine)

# Crear usuario docente de prueba si no existe
from app.db.session import SessionLocal
from app.db.models import Usuario
from app.core.security import get_password_hash

def crear_usuario_docente_prueba():
    db = SessionLocal()
    try:
        email = "docente@demo.com"
        existe = db.query(Usuario).filter_by(email=email).first()
        if not existe:
            user = Usuario(
                nombre="Docente Demo",
                email=email,
                password_hash=get_password_hash("demo1234"),
                rol="DOCENTE"
            )
            db.add(user)
            db.commit()
            print("Usuario docente de prueba creado: docente@demo.com / demo1234")
    except Exception as e:
        print(f"Error creando usuario de prueba: {e}")
    finally:
        db.close()

crear_usuario_docente_prueba()

app = FastAPI(title=settings.APP_NAME)

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(cursos_router, prefix="/api/v1/cursos", tags=["cursos"])
app.include_router(notas_router, prefix="/api/v1/notas", tags=["notas"])
app.include_router(estudiantes_router, prefix="/api/v1/estudiantes", tags=["estudiantes"])
app.include_router(docentes_router, prefix="/api/v1", tags=["docentes"])

# Servir archivos estáticos
os.makedirs("uploaded_images", exist_ok=True)
app.mount("/uploaded_images", StaticFiles(directory="uploaded_images"), name="uploaded_images")

@app.get("/health")
def health():
    return {"status": "ok"}
