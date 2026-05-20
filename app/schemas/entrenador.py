from pydantic import BaseModel, Field
from typing import Optional


class EntrenadorCreate(BaseModel):
    usuario_id: int
    especialidad: Optional[str] = None
   
    class Config:
        json_schema_extra = {
            "example": {
                "usuario_id": 2,
                "especialidad": "CrossFit"
            }
        }

class EntrenadorUpdate(BaseModel):
    especialidad: Optional[str] = None
    activo: Optional[bool] = None

class EntrenadorResponse(BaseModel):
    id: int
    usuario_id: int
    especialidad: Optional[str] = None
    activo: bool
   
    class Config:
        from_attributes = True