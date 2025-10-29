from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# Tabla intermedia para la relación muchos-a-muchos
libros_autores = Table(
    "libros_autores",
    Base.metadata,
    Column("libro_id", Integer, ForeignKey("libros.id", ondelete="CASCADE"), primary_key=True),
    Column("autor_id", Integer, ForeignKey("autores.id", ondelete="CASCADE"), primary_key=True)
)


class Autor(Base):
    __tablename__ = "autores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    pais_origen = Column(String)
    anio_nacimiento = Column(Integer)

    libros = relationship("Libro", secondary=libros_autores, back_populates="autores")

class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    ISBN = Column(String, unique=True, index=True)
    anio_publicacion = Column(Integer)
    copias_disponibles = Column(Integer)

    autores = relationship("Autor", secondary=libros_autores, back_populates="libros")
