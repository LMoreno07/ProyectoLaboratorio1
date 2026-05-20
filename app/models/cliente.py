"""
Modelo ORM para la tabla 'clientes'
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base
from datetime import datetime


class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Relación uno a uno con usuarios
    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        unique=True,        # Un usuario solo puede ser UN cliente
        nullable=False
    )
    
    cedula = Column(
        String(20),
        unique=True,        # No puede haber dos cédulas iguales
        nullable=False,
        index=True          # Búsqueda rápida por cédula (control de acceso)
    )
    
    fecha_nacimiento = Column(Date, nullable=True)
    telefono = Column(String(20), nullable=True)
    direccion = Column(String(255), nullable=True)
    fecha_registro = Column(DateTime, default=datetime.now())
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="cliente")
#    membresias = relationship("Membresia", back_populates="cliente")
#    reservas = relationship("Reserva", back_populates="cliente")
#    accesos = relationship("ControlAcceso", back_populates="cliente")
#    evaluaciones = relationship("EvaluacionBiometrica", back_populates="cliente")
#    ventas = relationship("VentaTienda", back_populates="cliente")
    
    def __repr__(self):
        return f"<Cliente(id={self.id}, cedula='{self.cedula}')>"