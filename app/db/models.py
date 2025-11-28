from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, Text, func, Float
from sqlalchemy.orm import relationship
from app.db.base import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(String(20), nullable=False)  # ESTUDIANTE | DOCENTE
    imagen = Column(String(255), nullable=True)  # Ruta o URL de la imagen
    creado_en = Column(DateTime, server_default=func.now())

    cursos = relationship("Curso", back_populates="docente")

class Curso(Base):
    __tablename__ = "cursos"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True)
    docente_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    creado_en = Column(DateTime, server_default=func.now())

    docente = relationship("Usuario", back_populates="cursos")
    inscripciones = relationship("Inscripcion", back_populates="curso")

class Inscripcion(Base):
    __tablename__ = "inscripciones"
    id = Column(Integer, primary_key=True)
    estudiante_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    curso_id = Column(Integer, ForeignKey("cursos.id"), nullable=False)
    fecha_inscripcion = Column(DateTime, server_default=func.now())

    curso = relationship("Curso", back_populates="inscripciones")

    __table_args__ = (UniqueConstraint('estudiante_id', 'curso_id', name='uq_estudiante_curso'),)

class Nota(Base):
    __tablename__ = "notas"
    id = Column(Integer, primary_key=True)
    estudiante_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    curso_id = Column(Integer, ForeignKey("cursos.id"), nullable=False)
    nota = Column(Float, nullable=False)
    actualizado_en = Column(DateTime, server_default=func.now(), onupdate=func.now())
