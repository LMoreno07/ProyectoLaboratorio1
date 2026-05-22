from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base
from datetime import datetime


class Reserva(Base):
    __tablename__ = "reservas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    sesion_id = Column(Integer, ForeignKey("sesiones_programadas.id"), nullable=False)
    fecha_reserva = Column(DateTime, default=datetime.now())
    asistio = Column(Boolean, default=False)
    
    cliente = relationship("Cliente", back_populates="reservas")
    sesion = relationship("Sesion", back_populates="reservas")
    
    def __repr__(self):
        return f"<Reserva(id={self.id}, cliente={self.cliente_id}, sesion={self.sesion_id})>"