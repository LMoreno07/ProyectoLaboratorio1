from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models.evaluacion_biometrica import EvaluacionBiometrica
from app.models.cliente import Cliente
from app.models.entrenador import Entrenador
from app.schemas.evaluacion_biometrica import EvaluacionCreate, EvaluacionUpdate, EvaluacionResponse

router = APIRouter(prefix="/evaluaciones", tags=["Biométrico"])


@router.post("/", response_model=EvaluacionResponse, status_code=201)
def crear_evaluacion(datos: EvaluacionCreate, db: Session = Depends(get_db)):
    if not db.query(Cliente).filter(Cliente.id == datos.cliente_id).first():
        raise HTTPException(404, "Cliente no encontrado")
    if not db.query(Entrenador).filter(Entrenador.id == datos.entrenador_id).first():
        raise HTTPException(404, "Entrenador no encontrado")
    
    evaluacion = EvaluacionBiometrica(**datos.model_dump())
    db.add(evaluacion)
    db.commit()
    db.refresh(evaluacion)
    return evaluacion


@router.get("/", response_model=List[EvaluacionResponse])
def listar_evaluaciones(
    skip: int = 0,
    limit: int = 10,
    cliente_id: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(EvaluacionBiometrica)
    if cliente_id:
        query = query.filter(EvaluacionBiometrica.cliente_id == cliente_id)
    return query.order_by(EvaluacionBiometrica.fecha.desc()).offset(skip).limit(limit).all()


@router.get("/{evaluacion_id}", response_model=EvaluacionResponse)
def obtener_evaluacion(evaluacion_id: int, db: Session = Depends(get_db)):
    evaluacion = db.query(EvaluacionBiometrica).filter(EvaluacionBiometrica.id == evaluacion_id).first()
    if not evaluacion:
        raise HTTPException(404, "Evaluación no encontrada")
    return evaluacion


@router.patch("/{evaluacion_id}", response_model=EvaluacionResponse)
def actualizar_evaluacion(evaluacion_id: int, datos: EvaluacionUpdate, db: Session = Depends(get_db)):
    evaluacion = db.query(EvaluacionBiometrica).filter(EvaluacionBiometrica.id == evaluacion_id).first()
    if not evaluacion:
        raise HTTPException(404, "Evaluación no encontrada")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(evaluacion, campo, valor)
    db.commit()
    db.refresh(evaluacion)
    return evaluacion