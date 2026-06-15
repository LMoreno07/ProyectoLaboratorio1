from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from app.models.ticket_mantenimiento import TicketMantenimiento
from app.models.maquina import Maquina
from app.schemas.ticket_mantenimiento import TicketCreate, TicketResolucion


def abrir_ticket(db: Session, maquina_id: int, datos: TicketCreate):
    maquina = db.query(Maquina).filter(Maquina.id == maquina_id).first()
    if not maquina:
        raise HTTPException(404, "Máquina no encontrada")
    
    # Cambiar estado de la máquina a "En Mantenimiento"
    maquina.estado_operativo = "En Mantenimiento"
    
    ticket = TicketMantenimiento(
        maquina_id=maquina_id,
        descripcion_falla=datos.descripcion_falla,
        estado_ticket="Abierto"
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


def resolver_ticket(db: Session, ticket_id: int, datos: TicketResolucion):
    ticket = db.query(TicketMantenimiento).filter(TicketMantenimiento.id == ticket_id).first()
    if not ticket:
        raise HTTPException(404, "Ticket no encontrado")
    
    ticket.estado_ticket = "Resuelto"
    ticket.fecha_resolucion = datetime.utcnow()
    if datos.costo_reparacion is not None:
        ticket.costo_reparacion = datos.costo_reparacion
    
    # Restaurar estado de la máquina
    maquina = db.query(Maquina).filter(Maquina.id == ticket.maquina_id).first()
    if maquina:
        maquina.estado_operativo = "Activa"
    
    db.commit()
    db.refresh(ticket)
    return ticket


def listar_tickets(db: Session, skip: int = 0, limit: int = 10):
    return db.query(TicketMantenimiento).offset(skip).limit(limit).all()


def obtener_ticket(db: Session, ticket_id: int):
    ticket = db.query(TicketMantenimiento).filter(TicketMantenimiento.id == ticket_id).first()
    if not ticket:
        raise HTTPException(404, "Ticket no encontrado")
    return ticket