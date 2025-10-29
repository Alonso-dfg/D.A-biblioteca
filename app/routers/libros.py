from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import crud, schemas, database, modelos
from pydantic import BaseModel, Field

router = APIRouter(prefix="/libros", tags=["Libros"])

# Modelo completo para crear libro con autores opcionales
class LibroConAutores(BaseModel):
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

# Crear libro
@router.post("/", response_model=schemas.Libro)
def crear_libro(data: LibroConAutores, db: Session = Depends(database.get_db)):
    """
    Crea un libro y lo asocia con uno o varios autores si se proporcionan sus IDs.
    """
    try:
        autor_ids = data.autor_ids or []
        return crud.crear_libro(db=db, libro=data, autor_ids=autor_ids)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ✅ Obtener todos los libros
@router.get("/", response_model=List[schemas.Libro])
def obtener_libros(
    anio_publicacion: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db)
):
    if anio_publicacion:
        return crud.obtener_libros_por_anio(db, anio_publicacion, skip, limit)
    return crud.obtener_libros(db, skip, limit)

# ✅ Obtener libro por ID
@router.get("/{libro_id}", response_model=schemas.Libro)
def obtener_libro(libro_id: int, db: Session = Depends(database.get_db)):
    libro = crud.obtener_libro(db, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

# ✅ Actualizar libro
@router.put("/libros/{libro_id}", response_model=schemas.Libro, tags=["Libros"])
def actualizar_libro(libro_id: int, libro: schemas.LibroConAutores, db: Session = Depends(database.get_db)):
    try:
        actualizado = crud.actualizar_libro(db=db, libro_id=libro_id, libro_data=libro)
        if not actualizado:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        return actualizado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/libros/{libro_id}/autores", response_model=List[schemas.Autor], tags=["Libros"])
def obtener_autores_por_libro(libro_id: int, db: Session = Depends(database.get_db)):
    """
    Retorna todos los autores asociados a un libro específico.
    """
    libro = db.query(modelos.Libro).filter(modelos.Libro.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    return [crud._autor_to_schema(a) for a in libro.autores]


# ✅ Eliminar libro
@router.delete("/{libro_id}", response_model=schemas.Libro)
def eliminar_libro(libro_id: int, db: Session = Depends(database.get_db)):
    eliminado = crud.eliminar_libro(db, libro_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return eliminado

