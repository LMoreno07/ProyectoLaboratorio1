from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base


class EvaluacionBiometrica(Base):
    __tablename__ = "evaluaciones_biometricas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    entrenador_id = Column(Integer, ForeignKey("entrenadores.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    peso_kg = Column(Numeric(5, 2), nullable=True)
    estatura_cm = Column(Numeric(5, 2), nullable=True)
    porcentaje_grasa = Column(Numeric(5, 2), nullable=True)
    observaciones = Column(String(255), nullable=True)
    
    cliente = relationship("Cliente", back_populates="evaluaciones")
    entrenador = relationship("Entrenador", back_populates="evaluaciones")
    
    def __repr__(self):
        return f"<Evaluacion(id={self.id}, cliente={self.cliente_id}, fecha={self.fecha})>"