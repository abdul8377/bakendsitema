# Backend (FastAPI) — Sistema Educativo

## Requisitos
- Python 3.11+
- MySQL (local o remoto)

## Instalación rápida
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Variables de entorno (ajusta credenciales):
copy .env.example .env        # Windows PowerShell
# o: cp .env.example .env     # Linux/macOS

# Crear tablas (SQLAlchemy) y arrancar API
uvicorn app.main:app --reload
```
API en: http://localhost:8000  |  Docs: http://localhost:8000/docs

## Migración de datos
- Si ya tienes la BD de Flask/MySQL, apunta `DATABASE_URL` a esa BD; SQLAlchemy mapeará las tablas si coinciden los nombres y tipos.
