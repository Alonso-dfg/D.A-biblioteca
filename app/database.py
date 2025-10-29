from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



#           --Configuración de la base de datos (SQLite)--

# Conexión a SQLite (archivo local)
SQLALCHEMY_DATABASE_URL = "sqlite:///./biblioteca.db"

# Creación del motor de conexión
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Creador de sesiones de base de datos
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Clase base para los modelos ORM
Base = declarative_base()


def get_db():
    """
    Proporciona una sesión de base de datos para usar en dependencias de FastAPI.

    Esta función es una dependencia típica utilizada con FastAPI.
    Crea una nueva sesión de base de datos, la entrega a la ruta que la requiere
    y garantiza su cierre una vez finalizada la operación, incluso si ocurre un error.

    Yield:
        Session: Objeto de sesión de SQLAlchemy para interactuar con la base de datos.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
