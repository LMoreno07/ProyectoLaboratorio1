from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models.pago import Pago
from app.models.membresia import Membresia
from app.schemas.pago import PagoCreate, PagoResponse

router = APIRouter(prefix="/pagos", tags=["Finanzas"])


@router.post("/", response_model=PagoResponse, status_code=201)
def registrar_pago(datos: PagoCreate, db: Session = Depends(get_db)):
    # Validar membresía existe
    membresia = db.query(Membresia).filter(Membresia.id == datos.membresia_id).first()
    if not membresia:
        raise HTTPException(404, "Membresía no encontrada")
    
    pago = Pago(**datos.model_dump())
    db.add(pago)
    db.commit()
    db.refresh(pago)
    return pago


@router.get("/", response_model=List[PagoResponse])
def listar_pagos(
    skip: int = 0,
    limit: int = 10,
    membresia_id: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(Pago)
    if membresia_id:
        query = query.filter(Pago.membresia_id == membresia_id)
    return query.offset(skip).limit(limit).all()


@router.get("/{pago_id}", response_model=PagoResponse)
def obtener_pago(pago_id: int, db: Session = Depends(get_db)):
    pago = db.query(Pago).filter(Pago.id == pago_id).first()
    if not pago:
        raise HTTPException(404, "Pago no encontrado")
    return pago