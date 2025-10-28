from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Ganado, Finca

router = APIRouter(
    prefix="/ganado",
    tags=["Ganado"]
)

# Crea una cabeza de ganado
@router.post("/")
def crear_ganado(nombre: str, edad: int, sexo: str, finca_id: int, db: Session = Depends(get_db)):
    finca = db.query(Finca).filter(Finca.id == finca_id).first()
    if not finca:
        raise HTTPException(status_code=404, detail="La finca no existe")

    nuevo_ganado = Ganado(nombre=nombre, edad=edad, sexo=sexo, finca_id=finca_id)
    db.add(nuevo_ganado)
    db.commit()
    db.refresh(nuevo_ganado)
    return {"mensaje": "Ganado creado correctamente", "ganado": nuevo_ganado}

# Muestra todos los ganados
@router.get("/")
def listar_ganado(db: Session = Depends(get_db)):
    ganados = db.query(Ganado).all()
    return ganados

# Busca ganado por id
@router.get("/{ganado_id}")
def obtener_ganado(ganado_id: int, db: Session = Depends(get_db)):
    ganado = db.query(Ganado).filter(Ganado.id == ganado_id).first()
    if not ganado:
        raise HTTPException(status_code=404, detail="Ganado no encontrado")
    return ganado

# Actualiza datos el ganado seleccionado
@router.put("/{ganado_id}")
def actualizar_ganado(ganado_id: int, nombre: str, edad: int, sexo: str, finca_id: int, db: Session = Depends(get_db)):
    ganado = db.query(Ganado).filter(Ganado.id == ganado_id).first()
    if not ganado:
        raise HTTPException(status_code=404, detail="Ganado no encontrado")

    finca = db.query(Finca).filter(Finca.id == finca_id).first()
    if not finca:
        raise HTTPException(status_code=404, detail="La finca asignada no existe")

    ganado.nombre = nombre
    ganado.edad = edad
    ganado.sexo = sexo
    ganado.finca_id = finca_id
    db.commit()
    db.refresh(ganado)
    return {"mensaje": "Ganado actualizado correctamente", "ganado": ganado}

#Modifica datos del ganado
@router.patch("/{ganado_id}")
def modificar_ganado(
    ganado_id: int,
    nombre: str = None,
    edad: int = None,
    sexo: str = None,
    finca_id: int = None,
    db: Session = Depends(get_db)
):
    ganado = db.query(Ganado).filter(Ganado.id == ganado_id).first()
    if not ganado:
        raise HTTPException(status_code=404, detail="Ganado no encontrado")

    if nombre:
        ganado.nombre = nombre
    if edad:
        ganado.edad = edad
    if sexo:
        ganado.sexo = sexo
    if finca_id:
        finca = db.query(Finca).filter(Finca.id == finca_id).first()
        if not finca:
            raise HTTPException(status_code=404, detail="La finca asignada no existe")
        ganado.finca_id = finca_id

    db.commit()
    db.refresh(ganado)
    return {"mensaje": "Ganado modificado correctamente", "ganado": ganado}

# Elimina la cabeza de ganado
@router.delete("/{ganado_id}")
def eliminar_ganado(ganado_id: int, db: Session = Depends(get_db)):
    ganado = db.query(Ganado).filter(Ganado.id == ganado_id).first()
    if not ganado:
        raise HTTPException(status_code=404, detail="Ganado no encontrado")

    db.delete(ganado)
    db.commit()
    return {"mensaje": "Ganado eliminado correctamente"}
