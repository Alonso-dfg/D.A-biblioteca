from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import modelos, schemas


# =====================================================
# 🔹 Funciones auxiliares (ORM → Schemas)
# =====================================================

def _autor_to_schema(a: modelos.Autor) -> schemas.Autor:
    """Convierte un Autor ORM a schemas.Autor, mostrando los títulos de sus libros."""
    return schemas.Autor(
        id=a.id,
        nombre=a.nombre,
        pais_origen=a.pais_origen,
        anio_nacimiento=a.anio_nacimiento,
        libros=[l.titulo for l in a.libros] if a.libros else []
    )


def _libro_to_schema(l: modelos.Libro) -> schemas.Libro:
    """Convierte un Libro ORM a schemas.Libro, mostrando los nombres de sus autores."""
    return schemas.Libro(
        id=l.id,
        titulo=l.titulo,
        ISBN=l.ISBN,
        anio_publicacion=l.anio_publicacion,
        copias_disponibles=l.copias_disponibles,
        autores=[a.nombre for a in l.autores] if l.autores else []
    )



# CRUD PARA AUTORES


def crear_autor(db: Session, autor: schemas.AutorCreate) -> schemas.Autor:
    db_autor = modelos.Autor(**autor.dict())
    db.add(db_autor)
    db.commit()
    db.refresh(db_autor)
    return _autor_to_schema(db_autor)


def obtener_autor(db: Session, autor_id: int) -> Optional[schemas.Autor]:
    autor = db.query(modelos.Autor).filter(modelos.Autor.id == autor_id).first()
    return _autor_to_schema(autor) if autor else None


def obtener_autores(
    db: Session,
    pais: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[schemas.Autor]:
    query = db.query(modelos.Autor)
    if pais:
        query = query.filter(modelos.Autor.pais_origen == pais)
    autores = query.offset(skip).limit(limit).all()
    return [_autor_to_schema(a) for a in autores]


def actualizar_autor(db: Session, autor_id: int, autor: schemas.AutorCreate) -> Optional[schemas.Autor]:
    db_autor = db.query(modelos.Autor).filter(modelos.Autor.id == autor_id).first()
    if db_autor:
        db_autor.nombre = autor.nombre
        db_autor.pais_origen = autor.pais_origen
        db_autor.anio_nacimiento = autor.anio_nacimiento
        db.commit()
        db.refresh(db_autor)
        return _autor_to_schema(db_autor)
    return None


def eliminar_autor(db: Session, autor_id: int) -> Optional[schemas.Autor]:
    db_autor = db.query(modelos.Autor).filter(modelos.Autor.id == autor_id).first()
    if db_autor:
        resultado = _autor_to_schema(db_autor)
        db.delete(db_autor)
        db.commit()
        return resultado
    return None



#CRUD PARA LIBROS


def crear_libro(db: Session, libro: schemas.LibroCreate, autor_ids: List[int]) -> schemas.Libro:
    """Crea un libro y lo asocia con los autores dados."""
    # ✅ Excluir autor_ids porque no es columna del modelo
    data = libro.dict(exclude={"autor_ids"}) if "autor_ids" in libro.dict() else libro.dict()
    db_libro = modelos.Libro(**data)

    # Asociar autores si se proporcionan IDs
    if autor_ids:
        autores = db.query(modelos.Autor).filter(modelos.Autor.id.in_(autor_ids)).all()
        if not autores:
            raise ValueError("No se encontraron autores con los IDs proporcionados.")
        db_libro.autores = autores

    try:
        db.add(db_libro)
        db.commit()
        db.refresh(db_libro)
    except IntegrityError:
        db.rollback()
        raise ValueError("El ISBN ya está registrado en otro libro.")

    return _libro_to_schema(db_libro)


def obtener_libros(db: Session, skip: int = 0, limit: int = 100) -> List[schemas.Libro]:
    libros = db.query(modelos.Libro).offset(skip).limit(limit).all()
    return [_libro_to_schema(l) for l in libros]


def obtener_libros_por_anio(
    db: Session,
    anio_publicacion: int,
    skip: int = 0,
    limit: int = 100
) -> List[schemas.Libro]:
    libros = (
        db.query(modelos.Libro)
        .filter(modelos.Libro.anio_publicacion == anio_publicacion)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [_libro_to_schema(l) for l in libros]


def obtener_libro(db: Session, libro_id: int) -> Optional[schemas.Libro]:
    libro = db.query(modelos.Libro).filter(modelos.Libro.id == libro_id).first()
    return _libro_to_schema(libro) if libro else None


def actualizar_libro(db: Session, libro_id: int, libro_data) -> Optional[schemas.Libro]:
    """
    Actualiza un libro existente y, si se envían nuevos autor_ids,
    actualiza también sus autores asociados.
    """
    db_libro = db.query(modelos.Libro).filter(modelos.Libro.id == libro_id).first()
    if not db_libro:
        return None

    # Excluir autor_ids del diccionario antes de actualizar campos
    data = libro_data.dict(exclude_unset=True, exclude={"autor_ids"})

    # Actualizar campos del libro
    for key, value in data.items():
        setattr(db_libro, key, value)

    # Si se proporcionan nuevos autores, actualizarlos
    if hasattr(libro_data, "autor_ids") and libro_data.autor_ids is not None:
        autores = db.query(modelos.Autor).filter(modelos.Autor.id.in_(libro_data.autor_ids)).all()
        if not autores and libro_data.autor_ids:
            raise ValueError("No se encontraron autores con los IDs proporcionados.")
        db_libro.autores = autores

    db.commit()
    db.refresh(db_libro)
    return _libro_to_schema(db_libro)


def eliminar_libro(db: Session, libro_id: int) -> Optional[schemas.Libro]:
    db_libro = db.query(modelos.Libro).filter(modelos.Libro.id == libro_id).first()
    if db_libro:
        resultado = _libro_to_schema(db_libro)
        db.delete(db_libro)
        db.commit()
        return resultado
    return None

