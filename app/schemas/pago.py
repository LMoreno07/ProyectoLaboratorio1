from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PagoCreate(BaseModel):
    membresia_id: int
    monto: float = Field(..., gt=0)
    metodo_pago: str
    referencia_externa: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "membresia_id": 1,
                "monto": 29.99,
                "metodo_pago": "Transferencia",
                "referencia_externa": "REF-12345"
            }
        }

class PagoResponse(BaseModel):
    id: int
    membresia_id: int
    monto: float
    fecha_pago: datetime
    metodo_pago: str
    referencia_externa: Optional[str] = None
    
    class Config:
        from_attributes = True