from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.reserva import Reserva
from app.models.sesion import Sesion
from app.models.cliente import Cliente
from app.schemas.reserva import ReservaCreate


def crear_reserva(db: Session, datos: ReservaCreate):
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
   
    # Validar cupo
    if sesion.cupos_ocupados >= sesion.cupo_maximo:
        raise HTTPException(409, "La sesión no tiene cupos disponibles")
   
    # Validar solapamiento de cliente
    conflicto_cliente = db.query(Reserva).join(Sesion).filter(
        Reserva.cliente_id == datos.cliente_id,
        Sesion.fecha == sesion.fecha,
        Sesion.hora_inicio < sesion.hora_fin,
        Sesion.hora_fin > sesion.hora_inicio
    ).first()
    if conflicto_cliente:
        raise HTTPException(409, "Ya tienes una reserva en ese horario")
   
    # Validar solapamiento de entrenador
    conflicto_entrenador = db.query(Reserva).join(Sesion).filter(
        Sesion.entrenador_id == sesion.entrenador_id,
        Sesion.fecha == sesion.fecha,
        Sesion.hora_inicio < sesion.hora_fin,
        Sesion.hora_fin > sesion.hora_inicio,
        Sesion.id != sesion.id
    ).first()
    if conflicto_entrenador:
        raise HTTPException(409, "El entrenador ya tiene una clase en ese horario")
   
    # Crear reserva
    reserva = Reserva(cliente_id=datos.cliente_id, sesion_id=datos.sesion_id)
    sesion.cupos_ocupados += 1
   
    db.add(reserva)
    db.commit()
    db.refresh(reserva)
    return reserva


def listar_reservas(db: Session, skip: int = 0, limit: int = 10, cliente_id: int = None, sesion_id: int = None):
    query = db.query(Reserva)
    if cliente_id:
        query = query.filter(Reserva.cliente_id == cliente_id)
    if sesion_id:
        query = query.filter(Reserva.sesion_id == sesion_id)
    return query.offset(skip).limit(limit).all()


def obtener_reserva(db: Session, reserva_id: int):
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if not reserva:
        raise HTTPException(404, "Reserva no encontrada")
    return reserva


def cancelar_reserva(db: Session, reserva_id: int):
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if not reserva:
        raise HTTPException(404, "Reserva no encontrada")
   
    sesion = db.query(Sesion).filter(Sesion.id == reserva.sesion_id).first()
    if sesion:
        sesion.cupos_ocupados -= 1
   
    db.delete(reserva)
    db.commit()