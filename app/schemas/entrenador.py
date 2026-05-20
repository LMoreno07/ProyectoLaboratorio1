<<<<<<< HEAD
from pydantic import BaseModel
from typing import Optional


class EntrenadorBase(BaseModel):
    usuario_id: int
    especialidad: Optional[str] = None
    activo: Optional[bool] = True


class EntrenadorCreate(EntrenadorBase):
    pass

=======
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
>>>>>>> c9029992fc74f960ee6197d43e9fb450ccf69db3

class EntrenadorUpdate(BaseModel):
    especialidad: Optional[str] = None
    activo: Optional[bool] = None

<<<<<<< HEAD

class EntrenadorResponse(EntrenadorBase):
    id: int

    class Config:
        from_attributes = True
=======
class EntrenadorResponse(BaseModel):
    id: int
    usuario_id: int
    especialidad: Optional[str] = None
    activo: bool
   
    class Config:
        from_attributes = True
>>>>>>> c9029992fc74f960ee6197d43e9fb450ccf69db3
