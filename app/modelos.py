from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base



#           --Tablas y modelos de la base de datos-


# Tabla intermedia para la relación muchos a muchos entre libros y autores
libros_autores = Table(
    "libros_autores",
    Base.metadata,
    Column("libro_id", Integer, ForeignKey("libros.id", ondelete="CASCADE"), primary_key=True),
    Column("autor_id", Integer, ForeignKey("autores.id", ondelete="CASCADE"), primary_key=True)
)


class Autor(Base):
    """
    Representa a un autor dentro de la base de datos.
    """
    __tablename__ = "autores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    pais_origen = Column(String)
    anio_nacimiento = Column(Integer)

    # Relación con los libros (muchos a muchos)
    libros = relationship("Libro", secondary=libros_autores, back_populates="autores")


class Libro(Base):
    """
    Representa un libro dentro de la base de datos.
    """
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    ISBN = Column(String, unique=True, index=True)
    anio_publicacion = Column(Integer)
    copias_disponibles = Column(Integer)

    # Relación con los autores (muchos a muchos)
    autores = relationship("Autor", secondary=libros_autores, back_populates="libros")

