from pydantic import BaseModel, Field
from typing import Optional


class DisciplinaCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    descripcion: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Yoga",
                "descripcion": "Clase de yoga para todos los niveles"
            }
        }

class DisciplinaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    descripcion: Optional[str] = None

class DisciplinaResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    
    class Config:
        from_attributes = True