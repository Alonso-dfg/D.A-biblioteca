from fastapi import FastAPI
from .database import Base, engine
from .routers import libros, autores

# Crear la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Biblioteca",
    description="Sistema de gestión de autores y libros (FastAPI + SQLite)",
    version="2.0"
)

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de Biblioteca"}

# Incluir routers
app.include_router(autores.router)
app.include_router(libros.router)
