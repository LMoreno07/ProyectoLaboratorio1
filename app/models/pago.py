from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base
from datetime import datetime


class Pago(Base):
    __tablename__ = "pagos"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    membresia_id = Column(Integer, ForeignKey("membresias.id"), nullable=False)
    monto = Column(Numeric(10, 2), nullable=False)
    fecha_pago = Column(DateTime, default=datetime.now())
    metodo_pago = Column(String(50), nullable=False)
    referencia_externa = Column(String(100), nullable=True)
    
    membresia = relationship("Membresia", back_populates="pagos")
    
    def __repr__(self):
        return f"<Pago(id={self.id}, monto={self.monto})>"