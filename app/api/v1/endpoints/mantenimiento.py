from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.models.database import get_db
from app.models.ticket_mantenimiento import TicketMantenimiento
from app.models.maquina import Maquina
from app.schemas.ticket_mantenimiento import TicketCreate, TicketResolucion, TicketResponse

router = APIRouter(prefix="/mantenimiento", tags=["Mantenimiento"])


@router.post("/maquinas/{maquina_id}/tickets", response_model=TicketResponse, status_code=201)
def abrir_ticket(maquina_id: int, datos: TicketCreate, db: Session = Depends(get_db)):
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


@router.patch("/tickets/{ticket_id}/resolver", response_model=TicketResponse)
def resolver_ticket(ticket_id: int, datos: TicketResolucion, db: Session = Depends(get_db)):
    ticket = db.query(TicketMantenimiento).filter(TicketMantenimiento.id == ticket_id).first()
    if not ticket:
        raise HTTPException(404, "Ticket no encontrado")
    
    ticket.estado_ticket = "Resuelto"
    ticket.fecha_resolucion = datetime.utcnow()
    if datos.costo_reparacion is not None:
        ticket.costo_reparacion = datos.costo_reparacion
    
    # Restaurar estado de la máquina
    maquina = db.query(Maquina).filter(Maquina.id == ticket.maquina_id).first()
    maquina.estado_operativo = "Activa"
    
    db.commit()
    db.refresh(ticket)
    return ticket


@router.get("/tickets", response_model=List[TicketResponse])
def listar_tickets(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(TicketMantenimiento).offset(skip).limit(limit).all()


@router.get("/tickets/{ticket_id}", response_model=TicketResponse)
def obtener_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(TicketMantenimiento).filter(TicketMantenimiento.id == ticket_id).first()
    if not ticket:
        raise HTTPException(404, "Ticket no encontrado")
    return ticket

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models.usuario import Usuario
from app.schemas.ticket_mantenimiento import TicketCreate, TicketResolucion, TicketResponse
from app.services.mantenimiento_services import (
    abrir_ticket as _abrir,
    resolver_ticket as _resolver,
    listar_tickets as _listar,
    obtener_ticket as _obtener
)
from app.core.dependencies import get_current_user, require_role

router = APIRouter(prefix="/mantenimiento", tags=["Mantenimiento"])


@router.post("/maquinas/{maquina_id}/tickets", response_model=TicketResponse, status_code=201)
def abrir_ticket(
    maquina_id: int,
    datos: TicketCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("Administrador"))
):
    """Abrir ticket de mantenimiento"""
    return _abrir(db, maquina_id, datos)


@router.patch("/tickets/{ticket_id}/resolver", response_model=TicketResponse)
def resolver_ticket(
    ticket_id: int,
    datos: TicketResolucion,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("Administrador"))
):
    """Resolver ticket."""
    return _resolver(db, ticket_id, datos)


@router.get("/tickets", response_model=List[TicketResponse])
def listar_tickets(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Listar tickets."""
    return _listar(db, skip, limit)


@router.get("/tickets/{ticket_id}", response_model=TicketResponse)
def obtener_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtener ticket por ID."""
    return _obtener(db, ticket_id)