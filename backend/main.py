from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db, engine, Base
from .schemas import UsuarioCreate, UsuarioDB, RecetaCreate, RecetaDB
from .crud import create_usuario, get_usuarios, create_receta, get_recetas
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

# Rutas para Recetas
@app.post("/recetas/", response_model=RecetaDB)
async def create_receta_endpoint(receta: RecetaCreate, db: AsyncSession = Depends(get_db)):
    return await create_receta(db, receta)

@app.get("/recetas/", response_model=list[RecetaDB])
async def get_recetas_endpoint(db: AsyncSession = Depends(get_db)):
    return await get_recetas(db)