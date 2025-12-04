from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
# Asegúrate de que estos imports apunten a tus archivos correctos
import models, schemas 
from database import get_db

# Inicializar Jinja2Templates (Asume que templates están en la carpeta 'templates')
templates = Jinja2Templates(directory="templates") 

router = APIRouter(
    prefix="/ganado",
    tags=["Ganado"]
)

# ============================================================
#                      RUTAS DE VISTAS (HTML GET)
# ============================================================

# 1. Muestra el formulario para registrar Ganado
# URL: /ganado/registrar
@router.get("/registrar") 
async def registrar_ganado_view(request: Request, db: Session = Depends(get_db)):
    """Muestra el formulario, cargando fincas y tipos de animales para los selects."""
    fincas = db.query(models.Finca).all()
    tipos_animales = db.query(models.TipoAnimal).all()
    
    return templates.TemplateResponse(
        "ganado/registrar_ganado.html", 
        {
            "request": request,
            "fincas": fincas,
            "tipos_animales": tipos_animales
        }
    )

# 2. Muestra la lista de Ganado
# URL: /ganado/lista
@router.get("/lista")
async def listar_ganado_view(request: Request, db: Session = Depends(get_db)):
    """Muestra la tabla de todo el ganado registrado, consultando la BD."""
    # Nota: Si el listado se vuelve lento, usa select_related en SQLA para cargar relaciones
    ganados = db.query(models.Ganado).all() 
    return templates.TemplateResponse(
        "ganado/lista_ganado.html",
        {"request": request, "ganados": ganados}
    )

# 3. Muestra el formulario para editar Ganado (precargado)
# URL: /ganado/editar/{ganado_id}
@router.get("/editar/{ganado_id}")
async def editar_ganado_view(ganado_id: int, request: Request, db: Session = Depends(get_db)):
    """Muestra el formulario de edición, precargando datos y listas de opciones."""
    ganado = db.query(models.Ganado).filter(models.Ganado.id == ganado_id).first()
    if not ganado:
        raise HTTPException(status_code=404, detail="Ganado no encontrado")
        
    fincas = db.query(models.Finca).all()
    tipos_animales = db.query(models.TipoAnimal).all()
    
    return templates.TemplateResponse(
        "ganado/editar_ganado.html",
        {
            "request": request,
            "ganado": ganado,
            "fincas": fincas,
            "tipos_animales": tipos_animales
        }
    )

# 4. Muestra el detalle de un animal
# URL: /ganado/detalle/{ganado_id}
@router.get("/detalle/{ganado_id}") 
async def detalle_ganado_view(ganado_id: int, request: Request, db: Session = Depends(get_db)):
    """Muestra el detalle de un animal específico."""
    ganado = db.query(models.Ganado).filter(models.Ganado.id == ganado_id).first()
    if not ganado:
        raise HTTPException(status_code=404, detail="Ganado no encontrado")
    
    return templates.TemplateResponse(
        "ganado/detalle_ganado.html",
        {"request": request, "ganado": ganado}
    )

# ============================================================
#                   RUTAS DE LA API (CRUD - JSON)
# ============================================================

# Crear ganado (POST API) - URL: /ganado/api/
@router.post("/api/", response_model=schemas.Ganado)
def crear_ganado(ganado: schemas.GanadoCreate, db: Session = Depends(get_db)):
    # Lógica de validación y creación...
    nuevo_ganado = models.Ganado(**ganado.dict())
    db.add(nuevo_ganado)
    db.commit()
    db.refresh(nuevo_ganado)
    return nuevo_ganado


# Listar ganado (GET API) - URL: /ganado/api/
@router.get("/api/", response_model=list[schemas.Ganado]) 
def listar_ganado_api(db: Session = Depends(get_db)):
    return db.query(models.Ganado).all()


# Actualizar/Modificar (PUT/PATCH) - URL: /ganado/api/{ganado_id}
# (Se asume que la lógica de actualización está implementada correctamente)


# Eliminar ganado (DELETE API) - URL: /ganado/api/{ganado_id}
@router.delete("/api/{ganado_id}") 
def eliminar_ganado(ganado_id: int, db: Session = Depends(get_db)):
    ganado = db.query(models.Ganado).filter(models.Ganado.id == ganado_id).first()
    if not ganado:
        raise HTTPException(status_code=404, detail="Ganado no encontrado")

    db.delete(ganado)
    db.commit()
    return {"mensaje": "Ganado eliminado correctamente"}