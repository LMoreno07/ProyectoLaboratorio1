"""
Modelo ORM (Objets relationship Mapping) para la tabla 'usuarios' 
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base
from datetime import datetime

class Usuario(Base):

    # Nombre de la tabla en la base de datos
    __tablename__ = "usuarios"

    # --- Columnas ---
    id = Column(
        Integer, 
        primary_key = True, 
        index=True
        )
    
    rol_id = Column(
        Integer, 
        ForeignKey("roles.id"), 
        nullable = False
        )
    
    email = Column(
        String(255), 
        unique=True, 
        nullable = False, 
        index = True
        )
    
    password_hash = Column(
        String(255), 
        nullable = False
        )
    
    nombre = Column(
        String(100), 
        nullable = False
        )
    
    apellido = Column(
        String(100), 
        nullable = False
        )
    
    activo = Column(
        Boolean, 
        default = True
        )
    
    created_at = Column(
        DateTime, 
        default = datetime.utcnow
        )

    # Relaciones
    # back_populates = "usuarios" se conecta con el atributo 'usuarios' en la clase Rol
    rol = relationship(
        "Rol",                          # Nombre de la clase relacionada
        back_populates = "usuarios"     # Atributo en Rol que apunta de vuelta a Usuario
        )
    
    cliente = relationship(
        "Cliente", 
        back_populates = "usuario", 
        uselist=False
        )
    
    
    entrenador = relationship(
        "Entrenador", 
        back_populates = "usuario", 
        uselist = False
        )
