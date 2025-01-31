## Instalación y Configuración
1. Clonar el repositorio:
   ```sh
   git clone https://github.com/Arlo-O/GestorRecetas.git
   cd GestorRecetas
   ```
2. Crear entorno virtual e instalar dependencias:
    En la carpeta del proyecto
   ```sh
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Ejecutar el backend con FastAPI:
   ```sh
   uvicorn backend.main:app --reload
   ```
4. Acceder a la documentación automática en `http://127.0.0.1:8000/docs`
