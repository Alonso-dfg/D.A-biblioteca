from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, database, modelos


#       --Rutas para gestionar autores--

router = APIRouter(prefix="/autores", tags=["Autores"])

#Crear un autor

@router.post("/", response_model=schemas.Autor)
def crear_autor(autor: schemas.AutorCreate, db: Session = Depends(database.get_db)):
    """
    Crea un nuevo autor en la base de datos.
    """
    return crud.crear_autor(db=db, autor=autor)

#Obtener autores

@router.get("/", response_model=List[schemas.Autor])
def obtener_autores(
    pais: str | None = None, skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)
):
    """
    Obtiene una lista de autores. Se puede filtrar por país.
    """
    return crud.obtener_autores(db=db, pais=pais, skip=skip, limit=limit)

#Obtener un autor

@router.get("/{autor_id}", response_model=schemas.Autor)
def obtener_autor(autor_id: int, db: Session = Depends(database.get_db)):
    """
    Obtiene un autor por su ID.
    """
    autor = crud.obtener_autor(db, autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return autor

#Actualizar autor

@router.put("/{autor_id}", response_model=schemas.Autor)
def actualizar_autor(autor_id: int, autor: schemas.AutorCreate, db: Session = Depends(database.get_db)):
    """
    Actualiza los datos de un autor existente.
    """
    actualizado = crud.actualizar_autor(db, autor_id, autor)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return actualizado


#Obtener libros por autor

@router.get("/autores/{autor_id}/libros", response_model=List[schemas.Libro], tags=["Autores"])
def obtener_libros_por_autor(autor_id: int, db: Session = Depends(database.get_db)):
    """
    Muestra los libros asociados a un autor específico.
    """
    autor = crud.obtener_autor(db, autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")

    libros = (
        db.query(modelos.Libro)
        .join(modelos.libros_autores)
        .filter(modelos.libros_autores.c.autor_id == autor_id)
        .all()
    )

    return [crud._libro_to_schema(l) for l in libros]


#Eliminar autor

@router.delete("/{autor_id}", response_model=schemas.Autor)
def eliminar_autor(autor_id: int, db: Session = Depends(database.get_db)):
    """
    Elimina un autor por su ID.
    """
    eliminado = crud.eliminar_autor(db, autor_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return eliminado


