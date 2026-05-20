from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class DetalleVentaCreate(BaseModel):
    producto_id: int
    cantidad: int = Field(..., gt=0)
    precio_unitario_aplicado: float = Field(..., gt=0)


class VentaCreate(BaseModel):
    cliente_id: Optional[int] = None
    metodo_pago: Optional[str] = None
    detalles: List[DetalleVentaCreate]
    
    class Config:
        json_schema_extra = {
            "example": {
                "cliente_id": 1,
                "metodo_pago": "Efectivo",
                "detalles": [
                    {"producto_id": 1, "cantidad": 2, "precio_unitario_aplicado": 5.99}
                ]
            }
        }


class DetalleVentaResponse(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_unitario_aplicado: float
    subtotal: float
    
    class Config:
        from_attributes = True


class VentaResponse(BaseModel):
    id: int
    cliente_id: Optional[int] = None
    fecha_venta: datetime
    total: float
    metodo_pago: Optional[str] = None
    detalles: List[DetalleVentaResponse] = []
    
    class Config:
        from_attributes = True