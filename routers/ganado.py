from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

# Inicializar Jinja2Templates
templates = Jinja2Templates(directory="templates") 

router = APIRouter(
    prefix="/ganado",
    tags=["Ganado"]
)

# ============================================================
#                      RUTAS DE VISTAS (HTML GET)
# ============================================================

# 1. Muestra el formulario para registrar Ganado (Crear)
# URL: /ganado/registrar
@router.get("/registrar") 
async def registrar_ganado_view(request: Request, db: Session = Depends(get_db)):
    """Muestra el formulario, cargando fincas y tipos de animales para los selects."""
    
    # Consulta los recursos necesarios para los selects del formulario
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
    
    # Consulta que incluye las relaciones para mostrar en la tabla
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
        
    # Consulta los recursos necesarios para los selects del formulario de edición
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
# URL: /ganado/{ganado_id}
# Nota: Esta ruta debe ir antes de cualquier GET de la API que use la misma URL
@router.get("/{ganado_id}")
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
#                   RUTAS DE LA API (CRUD EXISTENTE)
# ============================================================

# Crear ganado (POST API) - URL: /ganado/
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


# Listar ganado (GET API) - URL: /ganado/api/
@router.get("/api/", response_model=list[schemas.Ganado]) # RUTA MODIFICADA para evitar conflicto
def listar_ganado_api(db: Session = Depends(get_db)):
    return db.query(models.Ganado).all()


# Obtener ganado por ID (GET API) - URL: /ganado/{ganado_id}
@router.get("/{ganado_id}", response_model=schemas.Ganado)
def obtener_ganado_api(ganado_id: int, db: Session = Depends(get_db)):
    ganado = db.query(models.Ganado).filter(models.Ganado.id == ganado_id).first()
    if not ganado:
        raise HTTPException(status_code=404, detail="Ganado no encontrado")
    return ganado


# Actualizar ganado COMPLETO (PUT) - URL: /ganado/{ganado_id}
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


# Actualización parcial (PATCH) - URL: /ganado/{ganado_id}
@router.patch("/{ganado_id}", response_model=schemas.Ganado)
def modificar_ganado(
    ganado_id: int,
    datos: schemas.GanadoUpdate,
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


# Eliminar ganado (DELETE API) - URL: /ganado/{ganado_id}
@router.delete("/{ganado_id}")
def eliminar_ganado(ganado_id: int, db: Session = Depends(get_db)):
    ganado = db.query(models.Ganado).filter(models.Ganado.id == ganado_id).first()
    if not ganado:
        raise HTTPException(status_code=404, detail="Ganado no encontrado")

    db.delete(ganado)
    db.commit()
    return {"mensaje": "Ganado eliminado correctamente"}