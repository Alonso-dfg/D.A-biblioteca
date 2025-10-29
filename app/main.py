from fastapi import FastAPI
from .database import Base, engine
from .routers import libros, autores

#          --Configuración principal de la aplicación--

# Crea las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Inicializa la aplicación FastAPI
app = FastAPI(
    title="API Biblioteca",
    description="Sistema de biblioteca para gestionar Autores y Libros",
    version="1.0"
)

@app.get("/")
def root():
    """
    Muestra un mensaje de bienvenida al acceder a la ruta principal.
    """
    return {"message": "Bienvenido a la API de Biblioteca"}


# Incluye los routers de autores y libros
app.include_router(autores.router)
app.include_router(libros.router)

