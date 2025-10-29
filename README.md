# Proyecto de API de Biblioteca

Este proyecto es una API RESTful para gestionar **autores** y **libros** utilizando **FastAPI** y **SQLAlchemy** con una base de datos SQLite. Permite realizar operaciones CRUD sobre autores y libros, y permite filtrar los autores por país y los libros por año de publicación.

## Requisitos

Para ejecutar este proyecto, necesitas tener las siguientes dependencias instaladas:

- **Python 3.7+**
- **FastAPI**: Para crear la API.
- **SQLAlchemy**: Para la manipulación de la base de datos.
- **SQLite**: Base de datos usada para este proyecto (se crea automáticamente).
- **Uvicorn**: Servidor ASGI para correr FastAPI.
- **Pydantic**: Para validación de datos.

Puedes instalar las dependencias usando el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
