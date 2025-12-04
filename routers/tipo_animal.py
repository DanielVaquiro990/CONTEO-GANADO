from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
import models, schemas # Importa modelos y esquemas
from sqlalchemy.exc import IntegrityError # 🛑 IMPORTA ESTO


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
    # Nota: Tu esquema TipoAnimalCreate debe tener solo el campo 'nombre'

    nuevo_tipo = models.TipoAnimal(**tipo.dict())
    db.add(nuevo_tipo)
    
    try:
        db.commit() # Intentamos confirmar la inserción
    
    except IntegrityError as e:
        db.rollback() # Si hay error, revertimos la sesión
        
        # Verificamos si el error es por duplicidad (el constraint UNIQUE)
        # Esto funciona bien con SQLite y otros DBs
        if 'UNIQUE constraint failed' in str(e):
            raise HTTPException(
                status_code=400,
                detail=f"El Tipo de Animal con el nombre '{tipo.nombre}' ya existe."
            )
        else:
            # Captura cualquier otro error de integridad (ej: campo NOT NULL faltante)
            raise HTTPException(
                status_code=500,
                detail="Error de integridad de datos inesperado."
            )
    
    # Si el commit fue exitoso, refrescamos y retornamos
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


# En routers/tipo_animal.py, reemplaza la función existente por esta:
# Eliminar Tipo de Animal (DELETE API) - URL: /tipos-animales/{tipo_id}
@router.delete("/{tipo_id}") 
def eliminar_tipo_animal(tipo_id: int, db: Session = Depends(get_db)):
    
    # 1. Obtener el Tipo de Animal
    tipo = db.query(models.TipoAnimal).filter(models.TipoAnimal.id == tipo_id).first()
    
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de Animal no encontrado")

    # 2. 🛑 VERIFICAR GANADO DEPENDIENTE 🛑
    # Consulta la tabla de Ganado para ver si existe algún animal que use este tipo_animal_id
    ganado_dependiente = db.query(models.Ganado).filter(
        models.Ganado.tipo_animal_id == tipo_id
    ).first() 

    if ganado_dependiente:
        # Si se encuentra un animal, lanza la excepción HTTP 400 con el mensaje deseado
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar el tipo de animal porque se está usando."
        )

    # 3. Si no hay dependencias, proceder con la eliminación
    db.delete(tipo)
    
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        # Esto debería ser un error muy raro ahora, pero es bueno manejarlo
        raise HTTPException(status_code=500, detail=f"Error inesperado al eliminar: {e}")
        
    return {"mensaje": "Tipo de animal eliminado correctamente"}