from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime 
from database import Base

class Finca(Base):
    __tablename__ = "fincas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    tamaño = Column(Integer, nullable=False)
    ubicacion = Column(String(200), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    ganados = relationship(
        "Ganado", 
        back_populates="finca",
        cascade="all, delete-orphan"
    )

class TipoAnimal(Base):
    __tablename__ = "tipos_animales"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    ganados = relationship("Ganado", back_populates="tipo_animal")

class Ganado(Base):
    __tablename__ = "ganados"

    id = Column(Integer, primary_key=True, index=True)
    identificacion = Column(String, index=True, unique=True, nullable=False)
    nombre = Column(String(100), nullable=True)
    edad = Column(Integer, nullable=False)
    sexo = Column(String(10), nullable=False)
    finca_id = Column(Integer, ForeignKey("fincas.id"), nullable=False)
    tipo_animal_id = Column(Integer, ForeignKey("tipos_animales.id"), nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    finca = relationship("Finca", back_populates="ganados")
    tipo_animal = relationship("TipoAnimal", back_populates="ganados")
