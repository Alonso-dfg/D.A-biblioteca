from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, database

router = APIRouter(prefix="/autores", tags=["Autores"])

@router.post("/", response_model=schemas.Autor)
def crear_autor(autor: schemas.AutorCreate, db: Session = Depends(database.get_db)):
    return crud.crear_autor(db=db, autor=autor)

@router.get("/", response_model=List[schemas.Autor])
def obtener_autores(pais: str | None = None, skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.obtener_autores(db=db, pais=pais, skip=skip, limit=limit)

@router.get("/{autor_id}", response_model=schemas.Autor)
def obtener_autor(autor_id: int, db: Session = Depends(database.get_db)):
    autor = crud.obtener_autor(db, autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return autor

@router.put("/{autor_id}", response_model=schemas.Autor)
def actualizar_autor(autor_id: int, autor: schemas.AutorCreate, db: Session = Depends(database.get_db)):
    actualizado = crud.actualizar_autor(db, autor_id, autor)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return actualizado

@router.delete("/{autor_id}", response_model=schemas.Autor)
def eliminar_autor(autor_id: int, db: Session = Depends(database.get_db)):
    eliminado = crud.eliminar_autor(db, autor_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return eliminado

