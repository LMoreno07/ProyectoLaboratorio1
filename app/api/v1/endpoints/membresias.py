from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models.membresia import Membresia
from app.models.cliente import Cliente
from app.models.plan_suscripcion import PlanSuscripcion
from app.schemas.membresia import MembresiaCreate, MembresiaUpdate, MembresiaResponse

router = APIRouter(prefix="/membresias", tags=["Finanzas"])


@router.post("/", response_model=MembresiaResponse, status_code=201)
def crear_membresia(datos: MembresiaCreate, db: Session = Depends(get_db)):
    if not db.query(Cliente).filter(Cliente.id == datos.cliente_id).first():
        raise HTTPException(404, "Cliente no encontrado")
    if not db.query(PlanSuscripcion).filter(PlanSuscripcion.id == datos.plan_id).first():
        raise HTTPException(404, "Plan no encontrado")
    if datos.fecha_inicio >= datos.fecha_vencimiento:
        raise HTTPException(409, "La fecha de inicio debe ser menor a la de vencimiento")
    
    membresia = Membresia(**datos.model_dump())
    db.add(membresia)
    db.commit()
    db.refresh(membresia)
    return membresia


@router.get("/", response_model=List[MembresiaResponse])
def listar_membresias(
    skip: int = 0,
    limit: int = 10,
    cliente_id: int = None,
    estado: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Membresia)
    if cliente_id:
        query = query.filter(Membresia.cliente_id == cliente_id)
    if estado:
        query = query.filter(Membresia.estado == estado)
    return query.offset(skip).limit(limit).all()


@router.get("/{membresia_id}", response_model=MembresiaResponse)
def obtener_membresia(membresia_id: int, db: Session = Depends(get_db)):
    membresia = db.query(Membresia).filter(Membresia.id == membresia_id).first()
    if not membresia:
        raise HTTPException(404, "Membresía no encontrada")
    return membresia


@router.patch("/{membresia_id}", response_model=MembresiaResponse)
def actualizar_membresia(membresia_id: int, datos: MembresiaUpdate, db: Session = Depends(get_db)):
    membresia = db.query(Membresia).filter(Membresia.id == membresia_id).first()
    if not membresia:
        raise HTTPException(404, "Membresía no encontrada")
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(membresia, campo, valor)
    db.commit()
    db.refresh(membresia)
    return membresia