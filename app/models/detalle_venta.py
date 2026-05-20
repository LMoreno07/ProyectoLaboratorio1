from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base


class DetalleVenta(Base):
    __tablename__ = "detalle_ventas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    venta_id = Column(Integer, ForeignKey("ventas_tienda.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos_tienda.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario_aplicado = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
    
    venta = relationship("VentaTienda", back_populates="detalles")
    producto = relationship("ProductoTienda", back_populates="detalles")
    
    def __repr__(self):
        return f"<DetalleVenta(id={self.id}, cantidad={self.cantidad})>"