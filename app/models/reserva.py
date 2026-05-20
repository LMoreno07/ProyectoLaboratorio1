from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base

class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False) # Asumiendo que clientes son usuarios
    sesion_id = Column(Integer, ForeignKey("sesiones_programadas.id"), nullable=False)

    sesion = relationship("Sesion", back_populates="reservas")