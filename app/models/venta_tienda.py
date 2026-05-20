from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base
from datetime import datetime


class VentaTienda(Base):
    __tablename__ = "ventas_tienda"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=True)
    fecha_venta = Column(DateTime, default=datetime.utcnow)
    total = Column(Numeric(10, 2), nullable=False)
    metodo_pago = Column(String(50), nullable=True)
    
    cliente = relationship("Cliente", back_populates="ventas")
    detalles = relationship("DetalleVenta", back_populates="venta")
    
    def __repr__(self):
        return f"<Venta(id={self.id}, total={self.total})>"