from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .database import get_db, engine, Base
from .schemas import UsuarioCreate, UsuarioDB, RecetaCreate, RecetaDB
from .crud import (
    create_usuario, get_usuarios, delete_usuario, get_usuario,
    create_receta, get_recetas, delete_receta
)
from .prolog.consultas import obtener_recetas_por_dificultad, obtener_recetas_saludables, buscar_recetas_por_ingrediente
from .models import Usuario, Receta
app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Rutas para Usuarios
@app.post("/usuarios/", response_model=UsuarioDB)
async def create_usuario_endpoint(usuario: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    return await create_usuario(db, usuario)

@app.get("/usuarios/", response_model=list[UsuarioDB])
async def get_usuarios_endpoint(db: AsyncSession = Depends(get_db)):
    return await get_usuarios(db)

@app.get("/usuarios/{usuario_id}", response_model=UsuarioDB)
async def get_usuario_endpoint(usuario_id : int , db: AsyncSession = Depends(get_db)):
    usuario = await get_usuario(db, usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.delete("/usuarios/{usuario_id}")
async def delete_usuario_endpoint(usuario_id: int, db: AsyncSession = Depends(get_db)):
    usuario = await delete_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado"}

# Rutas para Recetas
@app.post("/recetas/", response_model=RecetaDB)
async def create_receta_endpoint(receta: RecetaCreate, db: AsyncSession = Depends(get_db)):
    return await create_receta(db, receta)

@app.get("/recetas/", response_model=list[RecetaDB])
async def get_recetas_endpoint(db: AsyncSession = Depends(get_db)):
    return await get_recetas(db)

@app.get("/recetas/filtradas", response_model=list[Receta])
async def get_recetas_filtradas(db: AsyncSession = Depends(get_db), tipo: str = None, ingrediente: str = None):
    recetas = await get_recetas(db)
    if tipo:
        recetas = obtener_recetas_por_dificultad(tipo)
    if ingrediente:
        recetas = buscar_recetas_por_ingrediente(ingrediente)
    return recetas

@app.delete("/recetas/{receta_id}")
async def delete_receta_endpoint(receta_id: int, db: AsyncSession = Depends(get_db)):
    receta = await delete_receta(db, receta_id)
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return {"message": "Receta eliminada"}

@app.get("/recetas/saludables/", response_model=list[str])
async def get_recetas_saludables_endpoint():
    try:
        recetas_saludables = obtener_recetas_saludables()
        return recetas_saludables
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener recetas saludables")

# Endpoint para buscar recetas por ingrediente
@app.get("/recetas/por_ingrediente/", response_model=list[str])
async def get_recetas_por_ingrediente_endpoint(ingrediente: str):
    try:
        recetas = buscar_recetas_por_ingrediente(ingrediente)
        return recetas
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al buscar recetas por ingrediente")

# Endpoint para obtener recetas sencillas o elaboradas
@app.get("/recetas/{tipo}/", response_model=list[str])
async def get_recetas_tipo_endpoint(tipo: str):
    if tipo not in ["sencilla", "elaborada"]:
        raise HTTPException(status_code=400, detail="Tipo de receta no válido")
    try:
        recetas = obtener_recetas_por_dificultad(tipo)
        return recetas
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener recetas sencillas o elaboradas")

@app.get("/")
async def root():
    return {"message": "API de Recetas funcionando"}
