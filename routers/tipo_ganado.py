from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas

router = APIRouter(
    prefix="/tipo-ganado",
    tags=["Tipo de Ganado"]
)

# ======================================================
#                   Crear Tipo de Ganado
# ======================================================
@router.post("/", response_model=schemas.TipoGanado)
def crear_tipo_ganado(tipo: schemas.TipoGanadoCreate, db: Session = Depends(get_db)):

    nuevo_tipo = models.TipoGanado(nombre=tipo.nombre)

    db.add(nuevo_tipo)
    db.commit()
    db.refresh(nuevo_tipo)

    return nuevo_tipo


# ======================================================
#         Obtener todos los Tipos de Ganado
# ======================================================
@router.get("/", response_model=list[schemas.TipoGanado])
def obtener_tipos(db: Session = Depends(get_db)):
    return db.query(models.TipoGanado).all()


# ======================================================
#        Obtener un Tipo de Ganado por ID
# ======================================================
@router.get("/{id}", response_model=schemas.TipoGanado)
def obtener_tipo(id: int, db: Session = Depends(get_db)):

    tipo = db.query(models.TipoGanado).filter(models.TipoGanado.id == id).first()

    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de ganado no encontrado")

    return tipo


# ======================================================
#                 Actualizar Tipo de Ganado
# ======================================================
@router.put("/{id}", response_model=schemas.TipoGanado)
def actualizar_tipo(id: int, datos: schemas.TipoGanadoCreate, db: Session = Depends(get_db)):

    tipo = db.query(models.TipoGanado).filter(models.TipoGanado.id == id).first()

    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de ganado no encontrado")

    tipo.nombre = datos.nombre

    db.commit()
    db.refresh(tipo)

    return tipo


# ======================================================
#                 Eliminar Tipo de Ganado
# ======================================================
@router.delete("/{id}")
def eliminar_tipo(id: int, db: Session = Depends(get_db)):

    tipo = db.query(models.TipoGanado).filter(models.TipoGanado.id == id).first()

    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de ganado no encontrado")

    db.delete(tipo)
    db.commit()

    return {"mensaje": "Tipo de ganado eliminado correctamente"}
