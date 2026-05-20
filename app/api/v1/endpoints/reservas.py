from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models.reserva import Reserva
from app.models.sesion import Sesion
from app.models.cliente import Cliente
from app.schemas.reserva import ReservaCreate, ReservaResponse

router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.post("/", response_model=ReservaResponse, status_code=201)
def crear_reserva(datos: ReservaCreate, db: Session = Depends(get_db)):
    # Validar cliente
    cliente = db.query(Cliente).filter(Cliente.id == datos.cliente_id).first()
    if not cliente:
        raise HTTPException(404, "Cliente no encontrado")
    
    # Validar sesión
    sesion = db.query(Sesion).filter(Sesion.id == datos.sesion_id).first()
    if not sesion:
        raise HTTPException(404, "Sesión no encontrada")
    if not sesion.activa:
        raise HTTPException(409, "La sesión no está activa")
    
    # Validación 1: Cupo disponible
    if sesion.cupos_ocupados >= sesion.cupo_maximo:
        raise HTTPException(409, "La sesión no tiene cupos disponibles")
    
    # Validación 2: Solapamiento de CLIENTE
    conflicto = db.query(Reserva).join(Sesion).filter(
        Reserva.cliente_id == datos.cliente_id,
        Sesion.fecha == sesion.fecha,
        Sesion.hora_inicio < sesion.hora_fin,
        Sesion.hora_fin > sesion.hora_inicio
    ).first()
    if conflicto:
        raise HTTPException(409, "Ya tienes una reserva en ese horario")
    
    # Validación 3: Solapamiento de ENTRENADOR
    entrenador_ocupado = db.query(Reserva).join(Sesion).filter(
        Sesion.entrenador_id == sesion.entrenador_id,
        Sesion.fecha == sesion.fecha,
        Sesion.hora_inicio < sesion.hora_fin,
        Sesion.hora_fin > sesion.hora_inicio
    ).first()
    if entrenador_ocupado:
        raise HTTPException(409, "El entrenador ya tiene una clase en ese horario")
    
    # Crear reserva y actualizar cupos
    reserva = Reserva(cliente_id=datos.cliente_id, sesion_id=datos.sesion_id)
    sesion.cupos_ocupados += 1
    
    db.add(reserva)
    db.commit()
    db.refresh(reserva)
    return reserva


@router.get("/", response_model=List[ReservaResponse])
def listar_reservas(
    skip: int = 0,
    limit: int = 10,
    cliente_id: int = None,
    sesion_id: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(Reserva)
    if cliente_id:
        query = query.filter(Reserva.cliente_id == cliente_id)
    if sesion_id:
        query = query.filter(Reserva.sesion_id == sesion_id)
    return query.offset(skip).limit(limit).all()


@router.get("/{reserva_id}", response_model=ReservaResponse)
def obtener_reserva(reserva_id: int, db: Session = Depends(get_db)):
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if not reserva:
        raise HTTPException(404, "Reserva no encontrada")
    return reserva


@router.delete("/{reserva_id}", status_code=204)
def cancelar_reserva(reserva_id: int, db: Session = Depends(get_db)):
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if not reserva:
        raise HTTPException(404, "Reserva no encontrada")
    
    # Liberar cupo
    sesion = db.query(Sesion).filter(Sesion.id == reserva.sesion_id).first()
    sesion.cupos_ocupados -= 1
    
    db.delete(reserva)
    db.commit()
    return None