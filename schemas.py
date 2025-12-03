from pydantic import BaseModel

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
