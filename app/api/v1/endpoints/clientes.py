"""
Endpoints para gestión de Clientes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.database import get_db
from app.models.cliente import Cliente
from app.models.usuario import Usuario
from app.models.evaluacion_biometrica import EvaluacionBiometrica
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from app.schemas.evaluacion_biometrica import EvaluacionCreate, EvaluacionResponse

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("/", response_model=ClienteResponse, status_code=201)
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == cliente.usuario_id).first()
    if not usuario:
        raise HTTPException(404, "Usuario no encontrado")
    
    existe = db.query(Cliente).filter(Cliente.usuario_id == cliente.usuario_id).first()
    if existe:
        raise HTTPException(409, "El usuario ya es un cliente")
    
    cedula_existe = db.query(Cliente).filter(Cliente.cedula == cliente.cedula).first()
    if cedula_existe:
        raise HTTPException(409, "La cédula ya está registrada")
    
    nuevo_cliente = Cliente(**cliente.model_dump())
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente


@router.get("/", response_model=List[ClienteResponse])
def listar_clientes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Cliente).offset(skip).limit(limit).all()


@router.get("/cedula/{cedula}", response_model=ClienteResponse)
def buscar_por_cedula(cedula: str, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.cedula == cedula).first()
    if not cliente:
        raise HTTPException(404, "Cliente no encontrado")
    return cliente


@router.get("/{cliente_id}", response_model=ClienteResponse)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(404, "Cliente no encontrado")
    return cliente


@router.patch("/{cliente_id}", response_model=ClienteResponse)
def actualizar_cliente(cliente_id: int, cliente_update: ClienteUpdate, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(404, "Cliente no encontrado")
    
    datos = cliente_update.model_dump(exclude_unset=True)
    for campo, valor in datos.items():
        setattr(cliente, campo, valor)
    
    db.commit()
    db.refresh(cliente)
    return cliente


@router.post("/{id}/evaluaciones", response_model=EvaluacionResponse, status_code=201)
def registrar_evaluacion(id: int, evaluacion: EvaluacionCreate, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not cliente:
        raise HTTPException(404, "Cliente no encontrado")
    
    nueva_ficha = EvaluacionBiometrica(
        cliente_id=id,
        entrenador_id=evaluacion.entrenador_id,
        fecha=evaluacion.fecha,
        peso_kg=evaluacion.peso_kg,
        estatura_cm=evaluacion.estatura_cm,
        porcentaje_grasa=evaluacion.porcentaje_grasa,
        observaciones=evaluacion.observaciones
    )
    
    db.add(nueva_ficha)
    db.commit()
    db.refresh(nueva_ficha)
    return nueva_ficha


@router.get("/{id}/evolucion", response_model=List[EvaluacionResponse])
def obtener_evolucion(id: int, db: Session = Depends(get_db)):
    historial = db.query(EvaluacionBiometrica)\
                  .filter(EvaluacionBiometrica.cliente_id == id)\
                  .order_by(EvaluacionBiometrica.fecha.desc())\
                  .all()
    return historial