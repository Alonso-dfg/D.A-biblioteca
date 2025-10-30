from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import crud, schemas, database, modelos
from pydantic import BaseModel, Field


#       --RUTAS PARA GESTIONAR LIBROS--


router = APIRouter(prefix="/libros", tags=["Libros"])



#MODELO EXTENDIDO PARA CREAR O ACTUALIZAR LIBROS

class LibroConAutores(BaseModel):
    """
    Modelo que permite crear o actualizar un libro con información
    básica y una lista opcional de IDs de autores ya existentes.

    Atributos:
        titulo (str): Título del libro.
        ISBN (str): Código único de identificación.
        anio_publicacion (int): Año en que fue publicado.
        copias_disponibles (int): Número de copias disponibles.
        autor_ids (List[int], opcional): IDs de autores asociados al libro.
    """
    titulo: str
    ISBN: str
    anio_publicacion: int
    copias_disponibles: int
    autor_ids: Optional[List[int]] = Field(
        default=None,
        description="Lista de IDs de autores existentes (ejemplo: [1, 2, 3])"
    )

    class Config:
        orm_mode = True


#CREAR LIBRO

@router.post("/", response_model=schemas.Libro)
def crear_libro(data: LibroConAutores, db: Session = Depends(database.get_db)):
    """
    Crea un nuevo libro en la base de datos.

    Si se incluyen IDs de autores, los asocia al libro recién creado.
    """
    try:
        autor_ids = data.autor_ids or []
        return crud.crear_libro(db=db, libro=data, autor_ids=autor_ids)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


#OBTENER TODOS LOS LIBROS

@router.get("/", response_model=List[schemas.Libro])
def obtener_libros(
        anio_publicacion: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(database.get_db)
):
    """
    Retorna la lista completa de libros disponibles.

    Si se indica un año de publicación, solo muestra los libros de ese año.
    """
    if anio_publicacion:
        return crud.obtener_libros_por_anio(db, anio_publicacion, skip, limit)
    return crud.obtener_libros(db, skip, limit)


# OBTENER LIBRO POR ID

@router.get("/{libro_id}", response_model=schemas.Libro)
def obtener_libro(libro_id: int, db: Session = Depends(database.get_db)):
    """
    Busca y devuelve un libro específico por su ID.
    """
    libro = crud.obtener_libro(db, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro


# ✏️ ACTUALIZAR LIBRO

@router.put("/libros/{libro_id}", response_model=schemas.Libro, tags=["Libros"])
def actualizar_libro(libro_id: int, libro: schemas.LibroUpdate, db: Session = Depends(database.get_db)):
    """
    Actualiza los datos de un libro existente.

    Permite cambiar:
      - Título
      - ISBN
      - Año de publicación
      - Copias disponibles
      - Autores asociados (si se envían nuevos IDs)
    """
    try:
        libro_actualizado = crud.actualizar_libro(db=db, libro_id=libro_id, libro_data=libro)
        if not libro_actualizado:
            raise HTTPException(status_code=404, detail="Libro no encontrado.")
        return libro_actualizado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# 👨‍🏫 OBTENER AUTORES DE UN LIBRO

@router.get("/libros/{libro_id}/autores", response_model=List[schemas.Autor], tags=["Libros"])
def obtener_autores_por_libro(libro_id: int, db: Session = Depends(database.get_db)):
    """
    Muestra los autores asociados a un libro específico.
    """
    libro = db.query(modelos.Libro).filter(modelos.Libro.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    return [crud._autor_to_schema(a) for a in libro.autores]


# ❌ ELIMINAR LIBRO

@router.delete("/libros/{libro_id}", response_model=schemas.Libro, tags=["Libros"])
def eliminar_libro(libro_id: int, db: Session = Depends(database.get_db)):
    """
    Elimina un libro por su ID.

    Reglas:
      - No se puede eliminar si el libro tiene copias disponibles (> 0).
      - Si no existe el libro, devuelve error 404.
    """
    try:
        libro_eliminado = crud.eliminar_libro(db=db, libro_id=libro_id)
        if not libro_eliminado:
            raise HTTPException(status_code=404, detail="Libro no encontrado.")
        return libro_eliminado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



