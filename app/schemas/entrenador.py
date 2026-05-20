from pydantic import BaseModel
from typing import Optional


class EntrenadorBase(BaseModel):
    usuario_id: int
    especialidad: Optional[str] = None
    activo: Optional[bool] = True


class EntrenadorCreate(EntrenadorBase):
    pass

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


class EntrenadorResponse(EntrenadorBase):
    id: int

    class Config:
        from_attributes = True
class EntrenadorResponse(BaseModel):
    id: int
    usuario_id: int
    especialidad: Optional[str] = None
    activo: bool
   
    class Config:
        from_attributes = True
