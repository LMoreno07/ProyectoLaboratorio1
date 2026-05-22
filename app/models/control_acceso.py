from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base
from datetime import datetime


class ControlAcceso(Base):
    __tablename__ = "control_accesos"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    fecha_hora_entrada = Column(DateTime, default=datetime.now())
    acceso_permitido = Column(Boolean, default=True)
    observaciones = Column(String(255), nullable=True)
    
    cliente = relationship("Cliente", back_populates="accesos")
    
    def __repr__(self):
        return f"<ControlAcceso(id={self.id}, permitido={self.acceso_permitido})>"