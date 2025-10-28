from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Finca(Base):
    __tablename__ = "fincas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    tamaño = Column(String)
    ubicacion = Column(String)

    ganados = relationship("Ganado", back_populates="finca")


class Ganado(Base):
    __tablename__ = "ganados"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    edad = Column(Integer)
    sexo = Column(String)
    finca_id = Column(Integer, ForeignKey("fincas.id"))

    # Relación inversa con Finca
    finca = relationship("Finca", back_populates="ganados")