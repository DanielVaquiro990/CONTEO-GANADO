from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
import models, schemas # Importa modelos y esquemas

# Inicializar Jinja2Templates
templates = Jinja2Templates(directory="templates") 

router = APIRouter(
    prefix="/tipos-animales", # Usamos guiones para la URL
    tags=["Tipos de Animales"]
)

# ======================================================
#                RUTAS DE VISTAS (HTML GET)
# ======================================================

# 1. Muestra el formulario para crear Tipo de Animal
# URL: /tipos-animales/crear
@router.get("/crear") 
async def crear_tipo_animal_view(request: Request):
    """Muestra el formulario para crear un nuevo tipo de animal."""
    return templates.TemplateResponse("tipo_animal/crear_tipo_animal.html", {"request": request})


# 2. Muestra la tabla de Tipos de Animales
# URL: /tipos-animales/lista
@router.get("/lista")
async def listar_tipos_animales_view(request: Request, db: Session = Depends(get_db)):
    """Muestra la tabla de tipos de animales."""
    tipos = db.query(models.TipoAnimal).all()
    return templates.TemplateResponse(
        "tipo_animal/lista_tipos_animales.html", 
        {"request": request, "tipos": tipos}
    )

# 3. Muestra el formulario para editar Tipo de Animal (precargado)
# URL: /tipos-animales/editar/{tipo_id}
@router.get("/editar/{tipo_id}")
async def editar_tipo_animal_view(tipo_id: int, request: Request, db: Session = Depends(get_db)):
    """Muestra el formulario de edición, precargando el nombre del tipo."""
    tipo = db.query(models.TipoAnimal).filter(models.TipoAnimal.id == tipo_id).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de animal no encontrado")
    return templates.TemplateResponse(
        "tipo_animal/editar_tipo_animal.html", 
        {"request": request, "tipo": tipo}
    )


# ======================================================
#                RUTAS DE LA API (CRUD EXISTENTE)
# ======================================================

# Crear Tipo de Animal (POST API) - URL: /tipos-animales/
@router.post("/", response_model=schemas.TipoAnimal)
def crear_tipo_animal(tipo: schemas.TipoAnimalCreate, db: Session = Depends(get_db)):
    nuevo_tipo = models.TipoAnimal(**tipo.dict())
    db.add(nuevo_tipo)
    db.commit()
    db.refresh(nuevo_tipo)
    return nuevo_tipo


# Listar todos los Tipos de Animales (GET API) - URL: /tipos-animales/
@router.get("/", response_model=list[schemas.TipoAnimal])
def listar_tipos_animales_api(db: Session = Depends(get_db)):
    """Devuelve datos JSON de todos los tipos de animales."""
    return db.query(models.TipoAnimal).all()


# Actualizar Tipo de Animal (PUT API) - URL: /tipos-animales/{tipo_id}
@router.put("/{tipo_id}", response_model=schemas.TipoAnimal)
def actualizar_tipo_animal(tipo_id: int, datos: schemas.TipoAnimalCreate, db: Session = Depends(get_db)):
    tipo = db.query(models.TipoAnimal).filter(models.TipoAnimal.id == tipo_id).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de animal no encontrado")

    for key, value in datos.dict().items():
        setattr(tipo, key, value)

    db.commit()
    db.refresh(tipo)
    return tipo


# Eliminar Tipo de Animal (DELETE API) - URL: /tipos-animales/{tipo_id}
@router.delete("/{tipo_id}")
def eliminar_tipo_animal(tipo_id: int, db: Session = Depends(get_db)):
    tipo = db.query(models.TipoAnimal).filter(models.TipoAnimal.id == tipo_id).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de animal no encontrado")

    db.delete(tipo)
    db.commit()
    return {"mensaje": "Tipo de animal eliminado correctamente"}