from pydantic import BaseModel
from typing import Optional
from datetime import date
from fastapi import UploadFile, File

# GanadoCreate se mantiene igual, sin la foto

#------Finca----

class FincaBase(BaseModel):
    nombre: str
    tamaño: int #Tamaño como entero (hectareas)
    ubicacion: str

class FincaCreate(FincaBase):
    pass

class Finca(FincaBase):
    id: int
    class Config:
        orm_mode = True


#-------Ganado------
class GanadoBase(BaseModel):
    identificacion: str
    nombre: Optional[str] = None
    fecha_nacimiento: date
    edad: int
    sexo: str
    finca_id: int
    tipo_animal_id: int     #relación con TipoAnimal

class GanadoCreate(GanadoBase):
    pass

class Ganado(GanadoBase):
    id: int
    class Config:
        orm_mode = True

class GanadoUpdate(BaseModel):
    nombre: str | None = None
    edad: int | None = None
    sexo: str | None = None
    finca_id: int | None = None

    class Config:
        orm_mode = True


class GanadoUpdateData(BaseModel):
    identificacion: str
    nombre: Optional[str] = None
    fecha_nacimiento: date
    sexo: str
    finca_id: int
    tipo_animal_id: int

#-------Tipo de Animal------

class TipoAnimalBase(BaseModel):
    nombre: str

class TipoAnimalCreate(TipoAnimalBase):
    pass

class TipoAnimal(TipoAnimalBase):
    id: int

    class Config:
        from_attributes = True



