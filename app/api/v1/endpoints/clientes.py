"""
Endpoints para gestión de Clientes
"""
<<<<<<< HEAD
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
=======
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

>>>>>>> c9029992fc74f960ee6197d43e9fb450ccf69db3
from app.models.database import get_db
from app.models.cliente import Cliente
from app.models.usuario import Usuario
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
<<<<<<< HEAD
from app.schemas.evaluacion_biometrica import EvaluacionBiometricaCreate, EvaluacionBiometricaResponse
from app.models.evaluacion_biometrica import EvaluacionBiometrica
=======
>>>>>>> c9029992fc74f960ee6197d43e9fb450ccf69db3

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)


@router.post("/", response_model=ClienteResponse, status_code=201)
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    """Registrar un nuevo cliente en el sistema"""
    # Verificar que el usuario existe
    usuario = db.query(Usuario).filter(Usuario.id == cliente.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Verificar que el usuario no sea ya un cliente
    existe = db.query(Cliente).filter(Cliente.usuario_id == cliente.usuario_id).first()
    if existe:
        raise HTTPException(status_code=409, detail="El usuario ya es un cliente")
    
    # Verificar cédula única
    cedula_existe = db.query(Cliente).filter(Cliente.cedula == cliente.cedula).first()
    if cedula_existe:
        raise HTTPException(status_code=409, detail="La cédula ya está registrada")
    
    nuevo_cliente = Cliente(**cliente.model_dump())
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente


@router.get("/", response_model=List[ClienteResponse])
def listar_clientes(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Listar clientes con paginación"""
    return db.query(Cliente).offset(skip).limit(limit).all()


@router.get("/{cliente_id}", response_model=ClienteResponse)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Obtener un cliente por su ID"""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.get("/cedula/{cedula}", response_model=ClienteResponse)
def buscar_por_cedula(cedula: str, db: Session = Depends(get_db)):
    """Buscar cliente por número de cédula (para control de acceso)"""
    cliente = db.query(Cliente).filter(Cliente.cedula == cedula).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.patch("/{cliente_id}", response_model=ClienteResponse)
def actualizar_cliente(
    cliente_id: int,
    cliente_update: ClienteUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar datos de un cliente (parcial)"""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Solo actualizar los campos enviados
    datos = cliente_update.model_dump(exclude_unset=True)
    for campo, valor in datos.items():
        setattr(cliente, campo, valor)
    
    db.commit()
    db.refresh(cliente)
<<<<<<< HEAD
    return cliente

# Registrar una nueva evaluación para un cliente
@router.post("/{id}/evaluaciones", response_model=EvaluacionBiometricaResponse, status_code=status.HTTP_201_CREATED)
def registrar_evaluacion_biometrica(id: int, evaluacion: EvaluacionBiometricaCreate, db: Session = Depends(get_db)):
    # 1. Verificar que el cliente exista
    cliente = db.query(Usuario).filter(Usuario.id == id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El cliente solicitado no existe."
        )
    
    # ID del entrenador simulado temporalmente
    id_entrenador_logueado = 2 

    nueva_ficha = EvaluacionBiometrica(
        cliente_id=id,
        entrenador_id=id_entrenador_logueado,
        peso=evaluacion.peso,
        grasa=evaluacion.grasa,
        estatura=evaluacion.estatura
    )
    
    db.add(nueva_ficha)
    db.commit()
    db.refresh(nueva_ficha)
    return nueva_ficha


# Obtener el historial de evolución biométrica
@router.get("/{id}/evolucion", response_model=List[EvaluacionBiometricaResponse])
def obtener_evolucion_cliente(id: int, db: Session = Depends(get_db)):
    historial = db.query(EvaluacionBiometrica)\
                  .filter(EvaluacionBiometrica.cliente_id == id)\
                  .order_by(EvaluacionBiometrica.created_at.asc())\
                  .all()
    return historial
=======
    return cliente
>>>>>>> c9029992fc74f960ee6197d43e9fb450ccf69db3
