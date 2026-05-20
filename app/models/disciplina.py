from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.models.database import Base


class Disciplina(Base):
    __tablename__ = "disciplinas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(Text, nullable=True)
    
    sesiones = relationship("Sesion", back_populates="disciplina")
    
    def __repr__(self):
        return f"<Disciplina(id={self.id}, nombre='{self.nombre}')>"