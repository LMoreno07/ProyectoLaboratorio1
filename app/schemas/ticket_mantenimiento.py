from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TicketCreate(BaseModel):
    maquina_id: int
    descripcion_falla: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "maquina_id": 1,
                "descripcion_falla": "La caminadora hace ruido extraño al correr"
            }
        }


class TicketResolucion(BaseModel):
    costo_reparacion: Optional[float] = Field(None, ge=0)
    
    class Config:
        json_schema_extra = {
            "example": {"costo_reparacion": 150.00}
        }


class TicketResponse(BaseModel):
    id: int
    maquina_id: int
    fecha_reporte: datetime
    descripcion_falla: str
    fecha_resolucion: Optional[datetime] = None
    costo_reparacion: Optional[float] = None
    estado_ticket: str
    
    class Config:
        from_attributes = True