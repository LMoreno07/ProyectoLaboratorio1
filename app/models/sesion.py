from sqlalchemy import Column, Integer, String, Date, Time, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base


class Sesion(Base):
    __tablename__ = "sesiones_programadas"
   
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    disciplina_id = Column(Integer, ForeignKey("disciplinas.id"), nullable=False)
    entrenador_id = Column(Integer, ForeignKey("entrenadores.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    cupo_maximo = Column(Integer, nullable=False)
    cupos_ocupados = Column(Integer, default=0)
    activa = Column(Boolean, default=True)
   
    # Relaciones
    disciplina = relationship("Disciplina", back_populates="sesiones")
    entrenador = relationship("Entrenador", back_populates="sesiones")
    reservas = relationship("Reserva", back_populates="sesion")
   
    def __repr__(self):
        return f"<Sesion(id={self.id}, fecha={self.fecha}, cupos={self.cupos_ocupados}/{self.cupo_maximo})>"