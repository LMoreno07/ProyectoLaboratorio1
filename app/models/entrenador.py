from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base


class Entrenador(Base):
    __tablename__ = "entrenadores"
   
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True, nullable=False)
    especialidad = Column(String(100), nullable=True)
    activo = Column(Boolean, default=True)
   
    usuario = relationship("Usuario", back_populates="entrenador")
    #sesiones = relationship("SesionProgramada", back_populates="entrenador")
    sesiones = relationship("Sesion", back_populates="entrenador")
    evaluaciones = relationship("EvaluacionBiometrica", back_populates="entrenador")
   
    def __repr__(self):
        return f"<Entrenador(id={self.id}, especialidad='{self.especialidad}')>"
