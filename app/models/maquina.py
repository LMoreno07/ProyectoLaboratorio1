from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base


class Maquina(Base):
    __tablename__ = "maquinas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    categoria_id = Column(Integer, ForeignKey("categorias_maquinas.id"), nullable=False)
    nombre = Column(String(100), nullable=False)
    descripcion_tecnica = Column(String(255), nullable=True)
    estado_operativo = Column(String(30), default="Activa")
    fecha_adquisicion = Column(Date, nullable=True)
    ultima_revision = Column(Date, nullable=True)
    codigo_serial = Column(String(50), unique=True, nullable=True)
    
    categoria = relationship("CategoriaMaquina", back_populates="maquinas")
    tickets = relationship("TicketMantenimiento", back_populates="maquina")
    
    def __repr__(self):
        return f"<Maquina(id={self.id}, nombre='{self.nombre}')>"