from pyswip import Prolog

prolog = Prolog()

# Cargar las reglas de Prolog
prolog.consult("reglas.pl")

def obtener_recetas_saludables():
    query = "obtener_recetas_saludables(Recetas)"
    result = list(prolog.query(query))
    return [res["Recetas"] for res in result]

def buscar_recetas_por_ingrediente(ingrediente):
    query = f"buscar_recetas_por_ingrediente({ingrediente}, Recetas)"
    result = list(prolog.query(query))
    return [res["Recetas"] for res in result]

def obtener_recetas_sencillas_o_elaboradas(tipo):
    query = f"{tipo}(Receta)"
    result = list(prolog.query(query))
    return [res["Receta"] for res in result]
from pyswip import Prolog

prolog = Prolog()

# Cargar las reglas de Prolog
prolog.consult("reglas.pl")

def obtener_recetas_saludables():
    query = "obtener_recetas_saludables(Recetas)"
    result = list(prolog.query(query))
    return [res["Recetas"] for res in result]

def buscar_recetas_por_ingrediente(ingrediente):
    query = f"buscar_recetas_por_ingrediente({ingrediente}, Recetas)"
    result = list(prolog.query(query))
    return [res["Recetas"] for res in result]

def obtener_recetas_por_dificultad(tipo):
    query = f"{tipo}(Receta)"
    result = list(prolog.query(query))
    return [res["Receta"] for res in result]
