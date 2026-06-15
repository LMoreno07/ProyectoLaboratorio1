from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CategoriaMaquinaCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: Optional[str] = None
    class Config:
        json_schema_extra = {
            "example": {"nombre":"Cardio","descripcion":"Máquinas cardiovasculares"}
        }

class CategoriaMaquinaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2,max_length=100)
    descripcion: Optional[str] = None

class CategoriaMaquinaResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str

    class Config:
        from_attributes = True
        