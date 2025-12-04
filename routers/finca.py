from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

# Inicializar Jinja2Templates
templates = Jinja2Templates(directory="templates") 

router = APIRouter(
    prefix="/fincas",
    tags=["Fincas"]
)

# ======================================================
#                RUTAS DE VISTAS (HTML GET)
# ======================================================

# 1. Muestra el formulario para crear finca
# URL final: /fincas/crear
@router.get("/crear") 
async def crear_finca_view(request: Request):
    """Muestra el formulario en templates/finca/crear_finca.html."""
    return templates.TemplateResponse("finca/crear_finca.html", {"request": request})


# 2. Muestra la tabla de todas las fincas
# URL final: /fincas/lista
@router.get("/lista")
async def listar_fincas_view(request: Request, db: Session = Depends(get_db)):
    """Muestra la tabla de fincas."""
    fincas = db.query(models.Finca).all()
    return templates.TemplateResponse(
        "finca/lista_fincas.html", 
        {"request": request, "fincas": fincas}
    )

# 3. Muestra el formulario para editar finca
# URL final: /fincas/editar/{finca_id}
@router.get("/editar/{finca_id}")
async def editar_finca_view(request: Request, finca_id: int, db: Session = Depends(get_db)):
    """Muestra el formulario precargado para editar."""
    finca = db.query(models.Finca).filter(models.Finca.id == finca_id).first()
    if not finca:
        raise HTTPException(status_code=404, detail="Finca no encontrada")
    return templates.TemplateResponse(
        "finca/editar_finca.html", 
        {"request": request, "finca": finca}
    )

# 4. Muestra el detalle de una finca específica
# URL final: /fincas/{finca_id}
# Nota: Esta ruta debe ir después de /fincas/lista y /fincas/editar
@router.get("/{finca_id}")
async def detalle_finca_view(request: Request, finca_id: int, db: Session = Depends(get_db)):
    """Muestra el detalle de una finca."""
    finca = db.query(models.Finca).filter(models.Finca.id == finca_id).first()
    if not finca:
        raise HTTPException(status_code=404, detail="Finca no encontrada")
    return templates.TemplateResponse(
        "finca/detalle_finca.html", 
        {"request": request, "finca": finca}
    )

# ======================================================
#                RUTAS DE LA API (CRUD EXISTENTE)
# ======================================================

# Crear finca (POST API) - URL: /fincas/
@router.post("/", response_model=schemas.Finca)
def crear_finca(finca: schemas.FincaCreate, db: Session = Depends(get_db)):
    nueva_finca = models.Finca(**finca.dict())
    db.add(nueva_finca)
    db.commit()
    db.refresh(nueva_finca)
    return nueva_finca


# Listar todas las fincas (GET API) - URL: /fincas/
# Se ha renombrado para no chocar con la función de vista (listar_fincas_view)
@router.get("/", response_model=list[schemas.Finca])
def listar_fincas_api(db: Session = Depends(get_db)):
    return db.query(models.Finca).all()


# Buscar finca por ID (GET API) - URL: /fincas/{finca_id}
# Esta ruta comparte URL con la vista de detalle. Para ver el JSON, usa /docs
@router.get("/{finca_id}", response_model=schemas.Finca)
def obtener_finca_api(finca_id: int, db: Session = Depends(get_db)):
    finca = db.query(models.Finca).filter(models.Finca.id == finca_id).first()
    if not finca:
        raise HTTPException(status_code=404, detail="Finca no encontrada")
    return finca


# Actualizar finca completa (PUT API) - URL: /fincas/{finca_id}
#FUNCIÓN PUT PARA ACTUALIZAR LA FINCA
@router.put("/{finca_id}", response_model=schemas.Finca)
def actualizar_finca(finca_id: int, datos: schemas.FincaCreate, db: Session = Depends(get_db)):
    # ... (código para buscar la finca) ...

    # 2. Actualizar los campos con los nuevos datos
    for key, value in datos.dict().items():
        setattr(finca, key, value) 

    # 3. Intentar confirmar la transacción (Persistir los cambios en la DB)
    try:
        # 💡 CAMBIO/REFUERZO: Aseguramos que SQLAlchemy sepa que este objeto está 'dirty'
        db.add(finca) 
        db.commit() # Escribe los cambios a la base de datos
    
    except IntegrityError as e:
        # ... (manejo de errores de unicidad) ...
        db.rollback()
        # ...
    
    db.refresh(finca)
    return finca


# Actualización parcial (PATCH API) - URL: /fincas/{finca_id}
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


# Eliminar finca (DELETE API) - URL: /fincas/{finca_id}
@router.delete("/{finca_id}")
def eliminar_finca(finca_id: int, db: Session = Depends(get_db)):
    finca = db.query(models.Finca).filter(models.Finca.id == finca_id).first()
    if not finca:
        raise HTTPException(status_code=404, detail="Finca no encontrada")

    db.delete(finca)
    db.commit()
    return {"mensaje": "Finca eliminada correctamente"}