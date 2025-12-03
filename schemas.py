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

#-------Tipo de Animal------

class TipoAnimalBase(BaseModel):
    nombre: str
    descripcion: str | None = None #Opcional por si se quiere añadir mas información

class TipoAnimalCreate(TipoAnimalBase):
    pass

class TipoAnimal(TipoAnimalBase):
    id: int
    class Config:
        orm_mode = True
