# Sistema de Gestión de Biblioteca — FastAPI + SQLAlchemy + SQLite

Este proyecto implementa una **API RESTful** para la **gestión de una biblioteca**, desarrollada con **FastAPI**, **SQLAlchemy** y **SQLite**.  
Permite registrar, consultar, actualizar y eliminar **libros** y **autores**, manteniendo una relación *muchos a muchos* entre ambos.
---

## Requerimientos para este proyecto
- fastapi
- uvicorn
- sqlalchemy
- pydantic

---

## Características principales

CRUD completo para **Libros** y **Autores**  
Relación **muchos-a-muchos** entre libros y autores  
Validaciones automáticas con **Pydantic**  
Persistencia con **SQLite**  
Documentación automática con **Swagger UI** y **ReDoc**  
Consultas avanzadas:
- Obtener **libros de un autor**
- Obtener **autores de un libro**

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

