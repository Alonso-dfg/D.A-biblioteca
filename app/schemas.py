from pydantic import BaseModel
from typing import List, Optional



#       --Esquemas base (estructuras comunes)--


class LibroBase(BaseModel):
    """
    Datos básicos de un libro.
    """
    titulo: str
    ISBN: str
    anio_publicacion: int
    copias_disponibles: int

    class Config:
        orm_mode = True


class AutorBase(BaseModel):
    """
    Datos básicos de un autor.
    """
    nombre: str
    pais_origen: str
    anio_nacimiento: int

    class Config:
        orm_mode = True



#       --Esquemas para crear registros--


class LibroCreate(LibroBase):
    """
    Esquema para crear un libro (sin autores aún).
    """
    pass


class AutorCreate(AutorBase):
    """
    Esquema para crear un autor (sin libros aún).
    """
    pass



#       --Esquemas para leer datos completos--


class Libro(LibroBase):
    """
    Representa un libro con su ID y lista de autores.
    """
    id: int
    autores: Optional[List[str]] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class Autor(AutorBase):
    """
    Representa un autor con su ID y lista de libros.
    """
    id: int
    libros: Optional[List[str]] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True



#       --Esquema extendido (crear o actualizar con autores)--


class LibroConAutores(LibroBase):
    """
    Permite crear o actualizar un libro con IDs de autores asociados.
    """
    autor_ids: Optional[List[int]] = None  # IDs de autores



