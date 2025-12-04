from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(
    prefix="/ganado",
    tags=["Ganado"]
)

# Crear ganado
@router.post("/", response_model=schemas.Ganado)
def crear_ganado(ganado: schemas.GanadoCreate, db: Session = Depends(get_db)):

    # Verificar finca existente
    finca = db.query(models.Finca).filter(models.Finca.id == ganado.finca_id).first()
    if not finca:
        raise HTTPException(status_code=404, detail="La finca no existe")

    nuevo_ganado = models.Ganado(**ganado.dict())
    db.add(nuevo_ganado)
    db.commit()
    db.refresh(nuevo_ganado)
    return nuevo_ganado


# Listar ganado
@router.get("/", response_model=list[schemas.Ganado])
def listar_ganado(db: Session = Depends(get_db)):
    return db.query(models.Ganado).all()


# Obtener ganado por ID
@router.get("/{ganado_id}", response_model=schemas.Ganado)
def obtener_ganado(ganado_id: int, db: Session = Depends(get_db)):
    ganado = db.query(models.Ganado).filter(models.Ganado.id == ganado_id).first()
    if not ganado:
        raise HTTPException(status_code=404, detail="Ganado no encontrado")
    return ganado


# Actualizar ganado COMPLETO (PUT)
@router.put("/{ganado_id}", response_model=schemas.Ganado)
def actualizar_ganado(
    ganado_id: int,
    datos: schemas.GanadoCreate,
    db: Session = Depends(get_db)
):
    ganado = db.query(models.Ganado).filter(models.Ganado.id == ganado_id).first()
    if not ganado:
        raise HTTPException(status_code=404, detail="Ganado no encontrado")

    # Validar finca nueva
    finca = db.query(models.Finca).filter(models.Finca.id == datos.finca_id).first()
    if not finca:
        raise HTTPException(status_code=404, detail="La finca asignada no existe")

    for key, value in datos.dict().items():
        setattr(ganado, key, value)

    db.commit()
    db.refresh(ganado)
    return ganado


# Actualización parcial (PATCH)
@router.patch("/{ganado_id}", response_model=schemas.Ganado)
def modificar_ganado(
    ganado_id: int,
    datos: schemas.GanadoUpdate,  # ← Para PATCH
    db: Session = Depends(get_db)
):
    ganado = db.query(models.Ganado).filter(models.Ganado.id == ganado_id).first()
    if not ganado:
        raise HTTPException(status_code=404, detail="Ganado no encontrado")

    cambios = datos.dict(exclude_unset=True)

    # Si se envía un finca_id verificar que exista
    if "finca_id" in cambios:
        finca = db.query(models.Finca).filter(models.Finca.id == cambios["finca_id"]).first()
        if not finca:
            raise HTTPException(status_code=404, detail="La finca asignada no existe")

    # Aplicar los cambios
    for key, value in cambios.items():
        setattr(ganado, key, value)

    db.commit()
    db.refresh(ganado)
    return ganado


# Eliminar ganado
@router.delete("/{ganado_id}")
def eliminar_ganado(ganado_id: int, db: Session = Depends(get_db)):
    ganado = db.query(models.Ganado).filter(models.Ganado.id == ganado_id).first()
    if not ganado:
        raise HTTPException(status_code=404, detail="Ganado no encontrado")

    db.delete(ganado)
    db.commit()
    return {"mensaje": "Ganado eliminado correctamente"}
