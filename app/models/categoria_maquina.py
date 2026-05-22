from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class CategoriaMaquina(Base):

    __tablename__ = "categorias_maquinas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String (255), unique = True, nullable=False)
    descripcion = Column(String (500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    maquinas = relationship("Maquina", back_populates="categoria", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Categoria {self.nombre}>"