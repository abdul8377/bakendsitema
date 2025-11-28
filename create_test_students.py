from app.db.session import SessionLocal
from app.db.models import Usuario
from app.core.security import get_password_hash

def create_test_students():
    db = SessionLocal()
    try:
        students = [
            {"nombre": "Estudiante Uno", "email": "estudiante1@demo.com", "password": "password123"},
            {"nombre": "Estudiante Dos", "email": "estudiante2@demo.com", "password": "password123"},
            {"nombre": "Estudiante Tres", "email": "estudiante3@demo.com", "password": "password123"},
        ]

        for s in students:
            exists = db.query(Usuario).filter_by(email=s["email"]).first()
            if not exists:
                user = Usuario(
                    nombre=s["nombre"],
                    email=s["email"],
                    password_hash=get_password_hash(s["password"]),
                    rol="ESTUDIANTE"
                )
                db.add(user)
                print(f"Creado usuario: {s['email']}")
            else:
                print(f"Usuario ya existe: {s['email']}")
        
        db.commit()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_students()
