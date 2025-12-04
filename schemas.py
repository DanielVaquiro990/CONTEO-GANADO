from pydantic import BaseModel

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
    nombre: str
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


#-------Tipo de Animal------

class TipoAnimalBase(BaseModel):
    nombre: str

class TipoAnimalCreate(TipoAnimalBase):
    pass

class TipoAnimal(TipoAnimalBase):
    id: int

    class Config:
        from_attributes = True



