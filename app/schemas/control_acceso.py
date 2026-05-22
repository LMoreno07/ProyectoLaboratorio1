from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AccesoEntrada(BaseModel):
    cedula: str
    
    class Config:
        json_schema_extra = {
            "example": {"cedula": "12345678"}
        }


class ControlAccesoResponse(BaseModel):
    id: int
    cliente_id: int
    fecha_hora_entrada: datetime
    acceso_permitido: bool
    observaciones: Optional[str] = None
    
    class Config:
        from_attributes = True