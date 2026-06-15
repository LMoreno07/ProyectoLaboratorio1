from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models.usuario import Usuario
from app.schemas.reserva import ReservaCreate, ReservaResponse
from app.services.reserva_service import (
    crear_reserva as _crear_reserva,
    listar_reservas as _listar_reservas,
    obtener_reserva as _obtener_reserva,
    cancelar_reserva as _cancelar_reserva
)
from app.core.dependencies import get_current_user, require_role  #  Protección

router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.post("/", response_model=ReservaResponse, status_code=201)
def crear_reserva(
    datos: ReservaCreate, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)  #  Cliente autenticado
    ):
    """Crear una reserva. Solo usuarios autenticados (clientes)."""
    return _crear_reserva(db, datos)


@router.get("/", response_model=List[ReservaResponse])
def listar_reservas(
    skip: int = 0,
    limit: int = 10,
    cliente_id: int = None,
    sesion_id: int = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_role("Administrador"))  #  Solo Admin
    ):
    """Listar reservas. Solo Admin."""
    return _listar_reservas(db, skip, limit, cliente_id, sesion_id)


@router.get("/{reserva_id}", response_model=ReservaResponse)
def obtener_reserva(
    reserva_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)  #  Autenticado
    ):
    """Ver detalle de una reserva."""
    return _obtener_reserva(db, reserva_id)


@router.delete("/{reserva_id}", status_code=204)
def cancelar_reserva(
    reserva_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)  #  Cliente o Admin
    ):
    """Cancelar una reserva. Cliente (su propia reserva) o Admin."""
    _cancelar_reserva(db, reserva_id)