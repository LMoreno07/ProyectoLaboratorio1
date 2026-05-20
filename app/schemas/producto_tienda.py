from pydantic import BaseModel, Field
from typing import Optional


class ProductoCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: Optional[str] = None
    precio_unitario: float = Field(..., gt=0)
    stock_actual: int = Field(0, ge=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Botella de agua",
                "descripcion": "Botella reutilizable 750ml",
                "precio_unitario": 5.99,
                "stock_actual": 50
            }
        }

class ProductoUpdate(BaseModel):
    descripcion: Optional[str] = None
    precio_unitario: Optional[float] = Field(None, gt=0)
    stock_actual: Optional[int] = Field(None, ge=0)
    activo: Optional[bool] = None

class ProductoResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    precio_unitario: float
    stock_actual: int
    activo: bool
    
    class Config:
        from_attributes = True