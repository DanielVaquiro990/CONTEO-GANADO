from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Finca

router = APIRouter(
    prefix="/fincas",
    tags=["Fincas"]
)

# Crea finca
@router.post("/")
def crear_finca(nombre: str, tamaño: str, ubicacion: str, db: Session = Depends(get_db)):
    nueva_finca = Finca(nombre=nombre, tamaño=tamaño, ubicacion=ubicacion)
    db.add(nueva_finca)
    db.commit()
    db.refresh(nueva_finca)
    return {"mensaje": "Finca creada correctamente", "finca": nueva_finca}

# Muestra todas las fincas
@router.get("/")
def listar_fincas(db: Session = Depends(get_db)):
    fincas = db.query(Finca).all()
    return fincas

# Buscar finca por id
@router.get("/{finca_id}")
def obtener_finca(finca_id: int, db: Session = Depends(get_db)):
    finca = db.query(Finca).filter(Finca.id == finca_id).first()
    if not finca:
        raise HTTPException(status_code=404, detail="Finca no encontrada")
    return finca

# Modifica las listas
@router.put("/{finca_id}")
def actualizar_finca(finca_id: int, nombre: str, tamaño: str, ubicacion: str, db: Session = Depends(get_db)):
    finca = db.query(Finca).filter(Finca.id == finca_id).first()
    if not finca:
        raise HTTPException(status_code=404, detail="Finca no encontrada")

    finca.nombre = nombre
    finca.tamaño = tamaño
    finca.ubicacion = ubicacion
    db.commit()
    db.refresh(finca)
    return {"mensaje": "Finca actualizada correctamente", "finca": finca}

# Actualiza
@router.patch("/{finca_id}")
def modificar_parcialmente(finca_id: int, nombre: str = None, tamaño: str = None, ubicacion: str = None, db: Session = Depends(get_db)):
    finca = db.query(Finca).filter(Finca.id == finca_id).first()
    if not finca:
        raise HTTPException(status_code=404, detail="Finca no encontrada")

    if nombre:
        finca.nombre = nombre
    if tamaño:
        finca.tamaño = tamaño
    if ubicacion:
        finca.ubicacion = ubicacion

    db.commit()
    db.refresh(finca)
    return {"mensaje": "Finca modificada parcialmente", "finca": finca}

# Elimina una finca
@router.delete("/{finca_id}")
def eliminar_finca(finca_id: int, db: Session = Depends(get_db)):
    finca = db.query(Finca).filter(Finca.id == finca_id).first()
    if not finca:
        raise HTTPException(status_code=404, detail="Finca no encontrada")

    db.delete(finca)
    db.commit()
    return {"mensaje": "Finca eliminada correctamente"}
