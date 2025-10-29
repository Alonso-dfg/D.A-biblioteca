from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import modelos, schemas



#           --Funciones auxiliares ORM = Schemas--


def _autor_to_schema(a: modelos.Autor) -> schemas.Autor:
    """
    Convierte un objeto ORM de tipo Autor a su representación del esquema Pydantic.
    Args:
        a (modelos.Autor): Instancia ORM del autor.
    Returns:
        schemas.Autor: Representación del autor lista para ser devuelta al cliente.
    """
    return schemas.Autor(
        id=a.id,
        nombre=a.nombre,
        pais_origen=a.pais_origen,
        anio_nacimiento=a.anio_nacimiento,
        libros=[l.titulo for l in a.libros] if a.libros else []
    )


def _libro_to_schema(l: modelos.Libro) -> schemas.Libro:
    """
    Convierte un objeto ORM de tipo Libro a su representación del esquema Pydantic.
    Args:
        l (modelos.Libro): Instancia ORM del libro.
    Returns:
        schemas.Libro: Representación del libro lista para ser devuelta al cliente.
    """
    return schemas.Libro(
        id=l.id,
        titulo=l.titulo,
        ISBN=l.ISBN,
        anio_publicacion=l.anio_publicacion,
        copias_disponibles=l.copias_disponibles,
        autores=[a.nombre for a in l.autores] if l.autores else []
    )



#           --CRUD PARA AUTORES--


def crear_autor(db: Session, autor: schemas.AutorCreate) -> schemas.Autor:
    """
    Crea un nuevo autor en la base de datos.
    Args:
        db (Session): Sesión de la base de datos.
        autor (schemas.AutorCreate): Datos del autor a registrar.
    Returns:
        schemas.Autor: Autor creado con su ID asignado.
    """
    db_autor = modelos.Autor(**autor.dict())
    db.add(db_autor)
    db.commit()
    db.refresh(db_autor)
    return _autor_to_schema(db_autor)


def obtener_autor(db: Session, autor_id: int) -> Optional[schemas.Autor]:
    """
    Obtiene un autor por su ID.
    Args:
        db (Session): Sesión de la base de datos.
        autor_id (int): ID del autor a buscar.
    Returns:
        Optional[schemas.Autor]: Autor encontrado o None si no existe.
    """
    autor = db.query(modelos.Autor).filter(modelos.Autor.id == autor_id).first()
    return _autor_to_schema(autor) if autor else None


def obtener_autores(
    db: Session,
    pais: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[schemas.Autor]:
    """
    Obtiene una lista de autores, con opción de filtrar por país.
    Args:
        db (Session): Sesión de la base de datos.
        pais (Optional[str], optional): País de origen del autor. Defaults a None.
        skip (int, optional): Cantidad de registros a omitir. Defaults a 0.
        limit (int, optional): Cantidad máxima de registros a devolver. Defaults a 100.
    Returns:
        List[schemas.Autor]: Lista de autores encontrados.
    """
    query = db.query(modelos.Autor)
    if pais:
        query = query.filter(modelos.Autor.pais_origen == pais)
    autores = query.offset(skip).limit(limit).all()
    return [_autor_to_schema(a) for a in autores]


def actualizar_autor(db: Session, autor_id: int, autor: schemas.AutorCreate) -> Optional[schemas.Autor]:
    """
    Actualiza los datos de un autor existente.
    Args:
        db (Session): Sesión de la base de datos.
        autor_id (int): ID del autor a actualizar.
        autor (schemas.AutorCreate): Nuevos datos del autor.
    Returns:
        Optional[schemas.Autor]: Autor actualizado o None si no existe.
    """
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
    """
    Elimina un autor por su ID.
    Args:
        db (Session): Sesión de la base de datos.
        autor_id (int): ID del autor a eliminar.
    Returns:
        Optional[schemas.Autor]: Autor eliminado o None si no existe.
    """
    db_autor = db.query(modelos.Autor).filter(modelos.Autor.id == autor_id).first()
    if db_autor:
        resultado = _autor_to_schema(db_autor)
        db.delete(db_autor)
        db.commit()
        return resultado
    return None



#           -- CRUD PARA LIBROS --


def crear_libro(db: Session, libro: schemas.LibroCreate, autor_ids: List[int]) -> schemas.Libro:
    """
    Crea un libro y lo asocia con los autores indicados.
    Args:
        db (Session): Sesión de la base de datos.
        libro (schemas.LibroCreate): Datos del libro a registrar.
        autor_ids (List[int]): Lista de IDs de autores asociados.
    Raises:
        ValueError: Si no se encuentran autores con los IDs proporcionados.
        ValueError: Si el ISBN ya está registrado.
    Returns:
        schemas.Libro: Libro creado con los autores asociados.
    """
    data = libro.dict(exclude={"autor_ids"}) if "autor_ids" in libro.dict() else libro.dict()
    db_libro = modelos.Libro(**data)

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
    """
    Obtiene una lista de libros registrados.
    Args:
        db (Session): Sesión de la base de datos.
        skip (int, optional): Cantidad de registros a omitir. Defaults a 0.
        limit (int, optional): Cantidad máxima de registros a devolver. Defaults a 100.
    Returns:
        List[schemas.Libro]: Lista de libros encontrados.
    """
    libros = db.query(modelos.Libro).offset(skip).limit(limit).all()
    return [_libro_to_schema(l) for l in libros]


def obtener_libros_por_anio(
    db: Session,
    anio_publicacion: int,
    skip: int = 0,
    limit: int = 100
) -> List[schemas.Libro]:
    """
    Obtiene los libros publicados en un año específico.
    Args:
        db (Session): Sesión de la base de datos.
        anio_publicacion (int): Año de publicación del libro.
        skip (int, optional): Cantidad de registros a omitir. Defaults a 0.
        limit (int, optional): Cantidad máxima de registros a devolver. Defaults a 100.
    Returns:
        List[schemas.Libro]: Lista de libros del año indicado.
    """
    libros = (
        db.query(modelos.Libro)
        .filter(modelos.Libro.anio_publicacion == anio_publicacion)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [_libro_to_schema(l) for l in libros]


def obtener_libro(db: Session, libro_id: int) -> Optional[schemas.Libro]:
    """
    Obtiene un libro por su ID.
    Args:
        db (Session): Sesión de la base de datos.
        libro_id (int): ID del libro a buscar.
    Returns:
        Optional[schemas.Libro]: Libro encontrado o None si no existe.
    """
    libro = db.query(modelos.Libro).filter(modelos.Libro.id == libro_id).first()
    return _libro_to_schema(libro) if libro else None


def actualizar_libro(db: Session, libro_id: int, libro_data) -> Optional[schemas.Libro]:
    """
    Actualiza un libro existente, incluyendo los autores asociados si se especifican nuevos IDs.
    Args:
        db (Session): Sesión de la base de datos.
        libro_id (int): ID del libro a actualizar.
        libro_data (schemas.LibroUpdate): Nuevos datos del libro.
    Raises:
        ValueError: Si no se encuentran los autores indicados.
    Returns:
        Optional[schemas.Libro]: Libro actualizado o None si no existe.
    """
    db_libro = db.query(modelos.Libro).filter(modelos.Libro.id == libro_id).first()
    if not db_libro:
        return None

    data = libro_data.dict(exclude_unset=True, exclude={"autor_ids"})

    for key, value in data.items():
        setattr(db_libro, key, value)

    if hasattr(libro_data, "autor_ids") and libro_data.autor_ids is not None:
        autores = db.query(modelos.Autor).filter(modelos.Autor.id.in_(libro_data.autor_ids)).all()
        if not autores and libro_data.autor_ids:
            raise ValueError("No se encontraron autores con los IDs proporcionados.")
        db_libro.autores = autores

    db.commit()
    db.refresh(db_libro)
    return _libro_to_schema(db_libro)


def eliminar_libro(db: Session, libro_id: int) -> Optional[schemas.Libro]:
    """
    Elimina un libro de la base de datos por su ID.
    Args:
        db (Session): Sesión de la base de datos.
        libro_id (int): ID del libro a eliminar.
    Returns:
        Optional[schemas.Libro]: Libro eliminado o None si no existe.
    """
    db_libro = db.query(modelos.Libro).filter(modelos.Libro.id == libro_id).first()
    if db_libro:
        resultado = _libro_to_schema(db_libro)
        db.delete(db_libro)
        db.commit()
        return resultado
    return None


