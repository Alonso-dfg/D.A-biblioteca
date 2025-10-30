# Sistema de Gestión de Biblioteca — FastAPI + SQLAlchemy + SQLite

Este proyecto implementa una **API RESTful** para la **gestión de una biblioteca**, desarrollada con **FastAPI**, **SQLAlchemy** y **SQLite**.  
Permite registrar, consultar, actualizar y eliminar **libros** y **autores**, manteniendo una relación *muchos a muchos* entre ambos.
---

## Tecnologias utilizadas Python 3.10+
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn
- SQLite (Base de datos)

---

## Características principales

CRUD completo para **Libros** y **Autores**  
Relación **muchos-a-muchos** entre libros y autores  
Validaciones automáticas con **Pydantic**  
Persistencia con **SQLite**  
Documentación automática con **Swagger UI** y **ReDoc**  
Consultas avanzadas:
- Obtener libros de un autor
- Obtener autores de un libro

---

## Estructura del proyecto 

```
sistema-biblioteca/
│
├── app/
│   ├── __init__.py
│   ├── main.py                Punto de entrada principal (inicia FastAPI)
│   ├── database.py            Configuración de la base de datos SQLite
│   ├── modelos.py             Modelos SQLAlchemy: Libro, Autor y tabla intermedia
│   ├── schemas.py             Esquemas Pydantic para validación y respuesta
│   ├── crud.py                Lógica CRUD de la aplicación
│   └── routers/
│       ├── autores.py         Endpoints para gestionar autores
│       └── libros.py          Endpoints para gestionar libros
│
├── requirements.txt           Dependencias del proyecto
└── README.md                  Este archivo de documentación

```
---

## Instalación y ejecución
1. **Clonar el repositorio**
    ````
   git clone https://github.com/Alonso-dfg/D.A-biblioteca
   cd D.A-biblioteca
   ````

2. **Crear entorno virtual**
    ````
   python -m venv venv
   venv/scripts/activate  #En windows
   source venv/bin/activate   #En Linux 
   ````

3. **Instalar dependencias**
    ````
   pip install -r requirements.txt
    ````
4. **Ejecutar el servidor**
    ````
   uvicorn app.main:app --reload
   ````
___
## Endpoints principales
| Recurso | Método | Ruta | Descripción |
|----------|--------|------|-------------|
| Libros | GET | `/libros/` | Lista todos los libros |
| Libros | POST | `/libros/` | Crea un nuevo libro |
| Autores | GET | `/autores/` | Lista todos los autores |
| Autores | POST | `/autores/` | Crea un nuevo autor |
___
## Reglas del negocio
- No se puede eliminar un libro que tenga copias disponibles (`> 0`).
- No se puede registrar un libro con número negativo de copias.
- Los autores deben existir antes de asociarlos a un libro.
- Un ISBN no puede repetirse (único por libro).
- Los libros y autores tienen relación *muchos a muchos*.
   


