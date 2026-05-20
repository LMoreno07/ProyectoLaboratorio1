from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReservaCreate(BaseModel):
    cliente_id: int
    sesion_id: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "cliente_id": 1,
                "sesion_id": 1
            }
        }


class ReservaResponse(BaseModel):
    id: int
    cliente_id: int
    sesion_id: int
    fecha_reserva: datetime
    asistio: bool
    
    class Config:
        from_attributes = True