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
## Endpoints Libros
| Recurso | Método | Ruta | Descripción |
|----------|--------|------|-------------|
| Obtener todos los libros | GET | `/libros/` | Lista todos los libros |
| Crear libro | POST | `/libros/` | Crea un nuevo libro |
| Obtener libro por ID | GET | `/libros/{libro_id}` | Devuelve la información de un libro específico. |
| Actualizar libro | PUT | `/libros/{libro_id}` | Modifica los datos de un libro, incluyendo autores |
| Eliminar libro | DELETE | `/libros/{libro_id}` | Elimina un libro (solo si tiene 0 copias disponibles). |
| Obtener autores de un libro | GET | `/libros/{libro_id}/autores` | Lista los autores asociados a un libro.|

## Endpoints Autores
| **Recurso**  | **Metodo** | **Ruta** | **Descripción** |
|------------|--------|------|---------------|
| Obtener todos los autores | GET | `/autores/` | Lista todos los autores |
| Crear autor | POST | `/autores/` | Crea un nuevo autor |
| Obtener autor por ID | GET | `/autores/{autor_id}` | Devuelve la información de un autor específico. |
| Actualizar autor | PUT | `/autores/{autor_id}` | Actualiza los datos de un autor existente. |
| Eliminar autor | DELETE | `/autores/{autor_id}` | Elimina un autor de la base de datos. |
| Obtener libros de un autor | GET | `/autores/{autor_id}/libros` | Muestra todos los libros escritos por un autor. |
___
## Reglas del negocio
- No se puede eliminar un libro que tenga copias disponibles (`> 0`).
- No se puede registrar un libro con número negativo de copias.
- Los autores deben existir antes de asociarlos a un libro.
- Un ISBN no puede repetirse (único por libro).
- Los libros y autores tienen relación *muchos a muchos*.
___
## Ejemplos de uso de la API 
### Crear un autor 
````
{
  "nombre": "Gabriel García Márquez",
  "pais_origen": "Colombia",
  "anio_nacimiento": 1927
}
````
### Crear un libro con autores
````
{
  "titulo": "Cien años de soledad",
  "ISBN": "978-3-16-148410-0",
  "anio_publicacion": 1967,
  "copias_disponibles": 5,
  "autor_ids": [1]
}
````
### Obtener todos los libros 
````
{
    "id": 1,
    "titulo": "Cien años de soledad",
    "ISBN": "978-3-16-148410-0",
    "anio_publicacion": 1967,
    "copias_disponibles": 5,
    "autores": ["Gabriel García Márquez"]
  }
````
### Obtener libro por ID 
````
{
  "id": 1,
  "titulo": "Cien años de soledad",
  "ISBN": "978-3-16-148410-0",
  "anio_publicacion": 1967,
  "copias_disponibles": 5,
  "autores": ["Gabriel García Márquez"]
}
````
### Actualizar libro existente 
````
{
  "titulo": "El amor en los tiempos del cólera",
  "ISBN": "978-0-06-088328-7",
  "anio_publicacion": 1985,
  "copias_disponibles": 8,
  "autor_ids": [1]
}
````
#### Si el libro tiene copias disponibles (> 0), no se podrá eliminar.
Debes reducir las copias a 0 antes de eliminarlo.
### Obtener libros por autor 
````
 {
    "id": 1,
    "titulo": "Cien años de soledad",
    "ISBN": "978-3-16-148410-0",
    "anio_publicacion": 1967,
    "copias_disponibles": 5
  }
````
## Obtener autores de un libro 
````
  {
    "id": 1,
    "nombre": "Gabriel García Márquez",
    "pais_origen": "Colombia",
    "anio_nacimiento": 1927
  }
````
## Validación de eliminación 
### Si intentas eliminar un libro con copias disponibles, veras este mensaje: 
````
{
  "detail": "No se puede eliminar un libro que aún tiene copias disponibles."
}
````
## Ejemplo de error al crear un libro con autor existente 
````
{
  "detail": "No se encontraron autores con los IDs proporcionados."
}
````
___
## Clases principales y relaciones del sistema
El proyecto está basado en **dos entidades principales**: `Libro` y `Autor`.  
Estas clases están conectadas mediante una **relación muchos a muchos (N:M)**,  
lo que significa que:
- Un **libro puede tener varios autores**.  
- Un **autor puede haber escrito varios libros**.

### 📘 Clase `Libro`
Ubicación: `modelos.py`

```python
class Libro(Base):
    __tablename__ = 'libros'

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    ISBN = Column(String, unique=True)
    anio_publicacion = Column(Integer)
    copias_disponibles = Column(Integer)

    # Relación con los autores
    autores = relationship('Autor', secondary='libros_autores', back_populates='libros')
````
Descripción:
- Representa un libro dentro de la base de datos.
- Cada libro tiene su título, ISBN, año de publicación y número de copias.
- Se relaciona con los autores mediante una tabla intermedia llamada libros_autores.
### Clase `Autor`
Ubicación: `modelos.py`

````python
    class Autor(Base):
    __tablename__ = 'autores'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    pais_origen = Column(String)
    anio_nacimiento = Column(Integer)

    # Relación con los libros
    libros = relationship('Libro', secondary='libros_autores', back_populates='autores')
````
Descripción:
- Representa a un autor dentro de la base de datos.
- Contiene datos personales del autor como nombre, país y año de nacimiento.
- Está conectado con varios libros.
### Tabla intermedia `libros_autores`
Ubicación: `modelos.py`
````python 
libros_autores = Table(
    'libros_autores',
    Base.metadata,
    Column('libro_id', Integer, ForeignKey('libros.id', ondelete='CASCADE'), primary_key=True),
    Column('autor_id', Integer, ForeignKey('autores.id', ondelete='CASCADE'), primary_key=True)
)
````
Descripción:
- Es la tabla que une libros y autores.
- Guarda pares de IDs (libro_id, autor_id) para representar las relaciones.
- Si se elimina un libro o un autor, su relación también se borra (por el CASCADE).
---
## Autor
- **Proyecto:** Sistema de gestión de biblioteca
- **Autor:** Alonso-dfg
- **Año:** 2025
