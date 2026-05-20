from sqlalchemy import Column, Integer, String, Boolean, Numeric
from sqlalchemy.orm import relationship
from app.models.database import Base


class PlanSuscripcion(Base):
    __tablename__ = "planes_suscripcion"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(String(255), nullable=True)
    costo = Column(Numeric(10, 2), nullable=False)
    duracion_dias = Column(Integer, nullable=False)
    activo = Column(Boolean, default=True)
    
    membresias = relationship("Membresia", back_populates="plan")
    
    def __repr__(self):
        return f"<PlanSuscripcion(id={self.id}, nombre='{self.nombre}')>"