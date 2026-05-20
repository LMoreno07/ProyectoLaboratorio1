from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models.plan_suscripcion import PlanSuscripcion
from app.schemas.plan_suscripcion import PlanCreate, PlanUpdate, PlanResponse

router = APIRouter(prefix="/planes", tags=["Finanzas"])


@router.post("/", response_model=PlanResponse, status_code=201)
def crear_plan(datos: PlanCreate, db: Session = Depends(get_db)):
    existe = db.query(PlanSuscripcion).filter(PlanSuscripcion.nombre == datos.nombre).first()
    if existe:
        raise HTTPException(409, f"El plan '{datos.nombre}' ya existe")
    plan = PlanSuscripcion(**datos.model_dump())
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


@router.get("/", response_model=List[PlanResponse])
def listar_planes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(PlanSuscripcion).offset(skip).limit(limit).all()


@router.get("/{plan_id}", response_model=PlanResponse)
def obtener_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(PlanSuscripcion).filter(PlanSuscripcion.id == plan_id).first()
    if not plan:
        raise HTTPException(404, "Plan no encontrado")
    return plan


@router.patch("/{plan_id}", response_model=PlanResponse)
def actualizar_plan(plan_id: int, datos: PlanUpdate, db: Session = Depends(get_db)):
    plan = db.query(PlanSuscripcion).filter(PlanSuscripcion.id == plan_id).first()
    if not plan:
        raise HTTPException(404, "Plan no encontrado")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(plan, campo, valor)
    db.commit()
    db.refresh(plan)
    return plan