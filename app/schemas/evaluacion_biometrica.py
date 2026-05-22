from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class EvaluacionCreate(BaseModel):
    cliente_id: int
    entrenador_id: int
    fecha: date
    peso_kg: Optional[float] = Field(None, gt=0)
    estatura_cm: Optional[float] = Field(None, gt=0)
    porcentaje_grasa: Optional[float] = Field(None, ge=0, le=100)
    observaciones: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "cliente_id": 1,
                "entrenador_id": 1,
                "fecha": "2026-06-01",
                "peso_kg": 75.5,
                "estatura_cm": 175.0,
                "porcentaje_grasa": 18.5,
                "observaciones": "Buena evolución"
            }
        }


class EvaluacionUpdate(BaseModel):
    peso_kg: Optional[float] = Field(None, gt=0)
    estatura_cm: Optional[float] = Field(None, gt=0)
    porcentaje_grasa: Optional[float] = Field(None, ge=0, le=100)
    observaciones: Optional[str] = None


class EvaluacionResponse(BaseModel):
    id: int
    cliente_id: int
    entrenador_id: int
    fecha: date
    peso_kg: Optional[float] = None
    estatura_cm: Optional[float] = None
    porcentaje_grasa: Optional[float] = None
    observaciones: Optional[str] = None
    
    class Config:
        from_attributes = True