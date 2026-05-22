from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class MaquinaCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    codigo_serial: Optional[str] = Field(None, max_length=50)
    descripcion_tecnica: Optional[str] = None
    estado_operativo: Optional[str] = "Activa"
    fecha_adquisicion: Optional[date] = None
    categoria_id: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Caminadora Pro",
                "codigo_serial": "CM-2025-001",
                "descripcion_tecnica": "Caminadora eléctrica 5HP",
                "estado_operativo": "Activa",
                "fecha_adquisicion": "2025-01-15",
                "categoria_id": 1
            }
        }


class MaquinaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    codigo_serial: Optional[str] = Field(None, max_length=50)
    descripcion_tecnica: Optional[str] = None
    estado_operativo: Optional[str] = None
    fecha_adquisicion: Optional[date] = None
    ultima_revision: Optional[date] = None


class MaquinaResponse(BaseModel):
    id: int
    nombre: str
    codigo_serial: Optional[str] = None
    descripcion_tecnica: Optional[str] = None
    estado_operativo: str
    fecha_adquisicion: Optional[date] = None
    ultima_revision: Optional[date] = None
    categoria_id: int
    
    class Config:
        from_attributes = True