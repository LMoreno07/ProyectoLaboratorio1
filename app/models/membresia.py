from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base


class Membresia(Base):
    __tablename__ = "membresias"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("planes_suscripcion.id"), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    estado = Column(String(20), default="Activa")
    
    cliente = relationship("Cliente", back_populates="membresias")
    plan = relationship("PlanSuscripcion", back_populates="membresias")
    pagos = relationship("Pago", back_populates="membresia")
    
    def __repr__(self):
        return f"<Membresia(id={self.id}, estado='{self.estado}')>"