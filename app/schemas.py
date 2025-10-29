from pydantic import BaseModel
from typing import List, Optional

# =====================================================
# 🔹 ESQUEMAS BASE
# =====================================================

class LibroBase(BaseModel):
    titulo: str
    ISBN: str
    anio_publicacion: int
    copias_disponibles: int

    class Config:
        orm_mode = True


class AutorBase(BaseModel):
    nombre: str
    pais_origen: str
    anio_nacimiento: int

    class Config:
        orm_mode = True


# =====================================================
# 🔹 ESQUEMAS PARA CREAR
# =====================================================

class LibroCreate(LibroBase):
    """Usado para crear un libro sin incluir autores todavía"""
    pass


class AutorCreate(AutorBase):
    """Usado para crear un autor sin incluir libros todavía"""
    pass


# =====================================================
# 🔹 ESQUEMAS PARA LEER DATOS COMPLETOS
# =====================================================

class Libro(LibroBase):
    """Devuelve la información de un libro junto con los IDs de sus autores"""
    id: int
    autores: Optional[List[str]] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class Autor(AutorBase):
    """Devuelve la información de un autor junto con los IDs de sus libros"""
    id: int
    libros: Optional[List[str]] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


# =====================================================
# 🔹 ESQUEMA EXTENDIDO (para crear o actualizar libros con autores)
# =====================================================

class LibroConAutores(LibroBase):
    """
    Esquema extendido para crear o actualizar libros,
    permitiendo especificar los IDs de los autores asociados.
    """
    autor_ids: Optional[List[int]] = None  # IDs de autores


