from fastapi import FastAPI
from routers import finca, ganado
from database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/") #MENSAJE PARA DOMINIO LOCAL /8000
def inicio():
    return {"CONTROL DE GANADO"}


app.include_router(finca.router)
app.include_router(ganado.router)