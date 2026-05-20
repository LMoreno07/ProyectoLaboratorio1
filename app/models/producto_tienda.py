from sqlalchemy import Column, Integer, String, Boolean, Numeric
from sqlalchemy.orm import relationship
from app.models.database import Base


class ProductoTienda(Base):
    __tablename__ = "productos_tienda"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    stock_actual = Column(Integer, default=0, nullable=False)
    activo = Column(Boolean, default=True)
    
    detalles = relationship("DetalleVenta", back_populates="producto")
    
    def __repr__(self):
        return f"<Producto(id={self.id}, nombre='{self.nombre}', stock={self.stock_actual})>"