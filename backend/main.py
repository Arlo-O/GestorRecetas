from fastapi import FastAPI
from .database import engine, Base

app = FastAPI()

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "API de Recetas funcionando"}