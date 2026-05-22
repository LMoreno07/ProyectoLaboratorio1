from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base
from datetime import datetime


class TicketMantenimiento(Base):
    __tablename__ = "tickets_mantenimiento"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    maquina_id = Column(Integer, ForeignKey("maquinas.id"), nullable=False)
    fecha_reporte = Column(DateTime, default=datetime.utcnow)
    descripcion_falla = Column(String(255), nullable=False)
    fecha_resolucion = Column(DateTime, nullable=True)
    costo_reparacion = Column(Numeric(10, 2), nullable=True)
    estado_ticket = Column(String(20), default="Abierto")
    
    maquina = relationship("Maquina", back_populates="tickets")
    
    def __repr__(self):
        return f"<Ticket(id={self.id}, estado='{self.estado_ticket}')>"