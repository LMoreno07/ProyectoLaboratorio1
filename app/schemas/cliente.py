"""
Schemas Pydantic para validación de datos de Clientes
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


class ClienteCreate(BaseModel):
    """Datos para crear un nuevo cliente"""
    usuario_id: int
    cedula: str = Field(..., min_length=6, max_length=20)
    fecha_nacimiento: Optional[date] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "usuario_id": 1,
                "cedula": "12345678",
                "fecha_nacimiento": "1995-06-15",
                "telefono": "0414-1234567",
                "direccion": "Barquisimeto, Edo. Lara"
            }
        }


class ClienteUpdate(BaseModel):
    """Datos para actualizar un cliente (todos opcionales)"""
    cedula: Optional[str] = Field(None, min_length=6, max_length=20)
    fecha_nacimiento: Optional[date] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None


class ClienteResponse(BaseModel):
    """Datos que retorna la API al consultar un cliente"""
    id: int
    usuario_id: int
    cedula: str
    fecha_nacimiento: Optional[date] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    fecha_registro: datetime
    
    class Config:
        from_attributes = True