from pydantic import BaseModel, Field
from datetime import datetime

# Lo que envía el Entrenador desde Swagger
class EvaluacionBiometricaCreate(BaseModel):
    peso: float = Field(..., gt=0, description="Peso en kg", example=78.3)
    grasa: float = Field(..., ge=0, le=100, description="Porcentaje de grasa corporal", example=15.4)
    estatura: float = Field(..., gt=0, description="Estatura en metros", example=1.75)

# Lo que Swagger devuelve
class EvaluacionBiometricaResponse(BaseModel):
    id: int
    cliente_id: int
    entrenador_id: int
    peso: float
    grasa: float
    estatura: float
    created_at: datetime

    class Config:
        from_attributes = True