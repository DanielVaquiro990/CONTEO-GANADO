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
    fecha_creacion = Column(DateTime, default=datetime.utcnow) #Fechas para las creacion de fincas

    # Relación con Ganado
    ganados = relationship(
        "Ganado", 
        back_populates="finca",
        cascade="all, delete-orphan"
    )


class Ganado(Base):
    __tablename__ = "ganados"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    edad = Column(Integer, nullable=False)
    sexo = Column(String(10), nullable=False)
    finca_id = Column(Integer, ForeignKey("fincas.id"), nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow) #Fecha automatica para el registro de ganado

    # Relación inversa
    finca = relationship("Finca", back_populates="ganados")
    tipo_animal = relationship("TipoAnimal", back_populates="ganados")

class TipoAnimal(Base):
    __tablename__ = "tipos_animales"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)  # vaca, cerdo, caballo, etc.

    ganados = relationship("Ganado", back_populates="tipo_animal")
