from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(
    prefix="/fincas",
    tags=["Fincas"]
)

# Crear finca (usando schema)
@router.post("/", response_model=schemas.Finca)
def crear_finca(finca: schemas.FincaCreate, db: Session = Depends(get_db)):
    nueva_finca = models.Finca(**finca.dict())
    db.add(nueva_finca)
    db.commit()
    db.refresh(nueva_finca)
    return nueva_finca


# Listar todas las fincas
@router.get("/", response_model=list[schemas.Finca])
def listar_fincas(db: Session = Depends(get_db)):
    return db.query(models.Finca).all()


# Buscar finca por ID
@router.get("/{finca_id}", response_model=schemas.Finca)
def obtener_finca(finca_id: int, db: Session = Depends(get_db)):
    finca = db.query(models.Finca).filter(models.Finca.id == finca_id).first()
    if not finca:
        raise HTTPException(status_code=404, detail="Finca no encontrada")
    return finca


# Actualizar finca completa
@router.put("/{finca_id}", response_model=schemas.Finca)
def actualizar_finca(finca_id: int, datos: schemas.FincaCreate, db: Session = Depends(get_db)):
    finca = db.query(models.Finca).filter(models.Finca.id == finca_id).first()
    if not finca:
        raise HTTPException(status_code=404, detail="Finca no encontrada")

    for key, value in datos.dict().items():
        setattr(finca, key, value)

    db.commit()
    db.refresh(finca)
    return finca


# Actualización parcial
@router.patch("/{finca_id}", response_model=schemas.Finca)
def modificar_parcialmente(finca_id: int, datos: schemas.FincaCreate, db: Session = Depends(get_db)):
    finca = db.query(models.Finca).filter(models.Finca.id == finca_id).first()
    if not finca:
        raise HTTPException(status_code=404, detail="Finca no encontrada")

    datos_dict = datos.dict(exclude_unset=True)
    for key, value in datos_dict.items():
        setattr(finca, key, value)

    db.commit()
    db.refresh(finca)
    return finca


# Eliminar finca
@router.delete("/{finca_id}")
def eliminar_finca(finca_id: int, db: Session = Depends(get_db)):
    finca = db.query(models.Finca).filter(models.Finca.id == finca_id).first()
    if not finca:
        raise HTTPException(status_code=404, detail="Finca no encontrada")

    db.delete(finca)
    db.commit()
    return {"mensaje": "Finca eliminada correctamente"}
