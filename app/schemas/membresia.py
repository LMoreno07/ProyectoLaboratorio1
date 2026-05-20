from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class MembresiaCreate(BaseModel):
    cliente_id: int
    plan_id: int
    fecha_inicio: date
    fecha_vencimiento: date
    
    class Config:
        json_schema_extra = {
            "example": {
                "cliente_id": 1,
                "plan_id": 1,
                "fecha_inicio": "2026-06-01",
                "fecha_vencimiento": "2026-07-01"
            }
        }

class MembresiaUpdate(BaseModel):
    fecha_vencimiento: Optional[date] = None
    estado: Optional[str] = None

class MembresiaResponse(BaseModel):
    id: int
    cliente_id: int
    plan_id: int
    fecha_inicio: date
    fecha_vencimiento: date
    estado: str
    
    class Config:
        from_attributes = True