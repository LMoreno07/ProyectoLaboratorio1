"""
Configuración de la conexión a la base de datos usando SQLAlchemy
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Leer URL del entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# Crear el motor de base de datos
engine = create_engine(DATABASE_URL)

# Fábrica de sesiones: cada petición HTTP obtiene su propia sesión
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Clase base para todos los modelos ORM
Base = declarative_base()


def get_db():
    """
    Generador que provee una sesión de base de datos por petición.
   
    Se usa como dependencia en los endpoints de FastAPI:
        db: Session = Depends(get_db)
   
    La sesión se cierra automáticamente al finalizar la petición.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()