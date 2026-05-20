from pydantic import BaseModel, Field
from typing import Optional


class PlanCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: Optional[str] = None
    costo: float = Field(..., gt=0)
    duracion_dias: int = Field(..., gt=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Plan Mensual",
                "descripcion": "Acceso ilimitado por 30 días",
                "costo": 29.99,
                "duracion_dias": 30
            }
        }

class PlanUpdate(BaseModel):
    descripcion: Optional[str] = None
    costo: Optional[float] = Field(None, gt=0)
    duracion_dias: Optional[int] = Field(None, gt=0)
    activo: Optional[bool] = None

class PlanResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    costo: float
    duracion_dias: int
    activo: bool
    
    class Config:
        from_attributes = True