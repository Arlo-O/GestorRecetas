from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Usuario, Ingrediente, Receta
from .schemas import UsuarioCreate, RecetaCreate, IngredienteBase

async def get_usuarios(db: AsyncSession):
    result = await db.execute(select(Usuario))
    return result.scalars().all()

async def create_usuario(db: AsyncSession, usuario: UsuarioCreate):
    nuevo_usuario = Usuario(nombre=usuario.nombre, contraseña=usuario.contraseña)
    db.add(nuevo_usuario)
    await db.commit()
    await db.refresh(nuevo_usuario)
    return nuevo_usuario

async def get_recetas(db: AsyncSession):
    result = await db.execute(select(Receta))
    recetas = result.scalars().all()

    for receta in recetas:
        await db.refresh(receta, ["ingredientes", "usuario"])

    return recetas

async def create_receta(db: AsyncSession, receta_data: RecetaCreate):
    nueva_receta = Receta(
        nombre=receta_data.nombre,
        tiempo_preparacion=receta_data.tiempo_preparacion,
        usuario_id=receta_data.usuario_id
    )
    db.add(nueva_receta)
    await db.commit()
    await db.refresh(nueva_receta)
    ingredientes = [
        Ingrediente(nombre=ing.nombre, receta_id=nueva_receta.id) 
        for ing in receta_data.ingredientes
    ]
    db.add_all(ingredientes)
    await db.commit()
    await db.refresh(nueva_receta, ["ingredientes", "usuario"])
        
    return nueva_receta