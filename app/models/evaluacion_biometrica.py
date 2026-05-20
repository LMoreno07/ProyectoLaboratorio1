from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base

class EvaluacionBiometrica(Base):
    __tablename__ = "evaluaciones_biometricas"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    entrenador_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    # Métricas físicas exactas solicitadas en el RF8
    peso = Column(Float, nullable=False)        # En kilogramos
    grasa = Column(Float, nullable=False)       # Porcentaje de grasa corporal
    estatura = Column(Float, nullable=False)    # En metros
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    cliente = relationship("Usuario", foreign_keys=[cliente_id])
    entrenador = relationship("Usuario", foreign_keys=[entrenador_id])