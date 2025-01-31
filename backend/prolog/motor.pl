:- consult('reglas.pl').  % Cargar la base de conocimientos

% Función para obtener recetas saludables
obtener_recetas_saludables(Recetas) :-
    findall(Receta, saludable(Receta), Recetas).

% Función para obtener recetas con un ingrediente específico
buscar_recetas_por_ingrediente(Ingrediente, Recetas) :-
    findall(Receta, recetas_con_ingrediente(Ingrediente, Receta), Recetas).
