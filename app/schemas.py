from pydantic import BaseModel
from typing import List, Optional



# ESQUEMAS BASE (estructuras comunes)

class LibroBase(BaseModel):
    """
    Representa los datos básicos de un libro.
    """
    titulo: str
    ISBN: str
    anio_publicacion: int
    copias_disponibles: int

    class Config:
        orm_mode = True  # Permite convertir datos del ORM a este modelo


class AutorBase(BaseModel):
    """
    Representa los datos básicos de un autor.
    """
    nombre: str
    pais_origen: str
    anio_nacimiento: int

    class Config:
        orm_mode = True



# ESQUEMAS PARA CREAR REGISTROS

class LibroCreate(LibroBase):
    """
    Se usa para crear un libro (sin autores todavía).
    """
    pass


class AutorCreate(AutorBase):
    """
    Se usa para crear un autor (sin libros todavía).
    """
    pass



# ESQUEMAS PARA LEER REGISTROS COMPLETOS

class Libro(LibroBase):
    """
    Muestra un libro con su ID y los autores que tiene.
    """
    id: int
    autores: Optional[List[str]] = None  # Solo los nombres de autores

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class Autor(AutorBase):
    """
    Muestra un autor con su ID y los libros que escribió.
    """
    id: int
    libros: Optional[List[str]] = None  # Solo los títulos de libros

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


# ESQUEMAS EXTENDIDOS (crear o actualizar con autores)

class LibroConAutores(LibroBase):
    """
    Permite crear o actualizar un libro indicando los IDs de los autores.
    """
    autor_ids: Optional[List[int]] = None  # IDs de autores existentes


class LibroUpdate(BaseModel):
    """
    Se usa para actualizar un libro.
    Todos los campos son opcionales, así puedes cambiar solo uno.
    """
    titulo: Optional[str] = None
    ISBN: Optional[str] = None
    anio_publicacion: Optional[int] = None
    copias_disponibles: Optional[int] = None
    autor_ids: Optional[List[int]] = None  # IDs de autores nuevos (opcional)

    class Config:
        orm_mode = True


