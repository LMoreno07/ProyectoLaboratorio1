from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models.control_acceso import ControlAcceso
from app.models.cliente import Cliente
from app.models.membresia import Membresia
from app.schemas.control_acceso import AccesoEntrada, ControlAccesoResponse
from datetime import date

router = APIRouter(prefix="/accesos", tags=["Acceso"])


@router.post("/entrada", response_model=ControlAccesoResponse)
def registrar_entrada(datos: AccesoEntrada, db: Session = Depends(get_db)):
    # Buscar cliente por cédula
    cliente = db.query(Cliente).filter(Cliente.cedula == datos.cedula).first()
    if not cliente:
        raise HTTPException(404, "Cliente no encontrado")
    
    # Validar membresía activa
    membresia = db.query(Membresia).filter(
        Membresia.cliente_id == cliente.id,
        Membresia.estado == "Activa",
        Membresia.fecha_vencimiento >= date.today()
    ).first()
    
    if not membresia:
        acceso = ControlAcceso(
            cliente_id=cliente.id,
            acceso_permitido=False,
            observaciones="Membresía vencida o no activa"
        )
        db.add(acceso)
        db.commit()
        db.refresh(acceso)
        raise HTTPException(409, "Acceso denegado: Membresía vencida o no activa")
    
    # Acceso permitido
    acceso = ControlAcceso(
        cliente_id=cliente.id,
        acceso_permitido=True,
        observaciones="Acceso permitido"
    )
    db.add(acceso)
    db.commit()
    db.refresh(acceso)
    return acceso


@router.get("/", response_model=List[ControlAccesoResponse])
def listar_accesos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(ControlAcceso).order_by(ControlAcceso.fecha_hora_entrada.desc()).offset(skip).limit(limit).all()