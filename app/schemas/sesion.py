from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time


class SesionCreate(BaseModel):
    disciplina_id: int
    entrenador_id: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    cupo_maximo: int = Field(..., gt=0)
   
    class Config:
        json_schema_extra = {
            "example": {
                "disciplina_id": 1,
                "entrenador_id": 1,
                "fecha": "2026-06-01",
                "hora_inicio": "08:00",
                "hora_fin": "09:00",
                "cupo_maximo": 20
            }
        }

class SesionUpdate(BaseModel):
    fecha: Optional[date] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    cupo_maximo: Optional[int] = Field(None, gt=0)
    activa: Optional[bool] = None

class SesionResponse(BaseModel):
    id: int
    disciplina_id: int
    entrenador_id: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    cupo_maximo: int
    cupos_ocupados: int
    activa: bool
   
    class Config:
        from_attributes = True