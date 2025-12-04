from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
import models

# Routers
from routers import finca
from routers import ganado
from routers import tipo_ganado

# Crear tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Gestión de Ganado",
    description="API para administrar fincas, ganado y tipos de ganado",
    version="1.0.0"
)

# ============================================================
#                      CORS (opcional)
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # En producción debes especificar dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
#                    RUTAS (Routers)
# ============================================================
app.include_router(finca.router)
app.include_router(ganado.router)
app.include_router(tipo_ganado.router)

# ============================================================
#                        RUTA RAÍZ
# ============================================================
@app.get("/")
def root():
    return {"mensaje": "API de gestión de ganado funcionando correctamente"}
