"""
Punto de entrada principal de SmartGym API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core import settings
from app.models.database import Base, engine
from app.api.v1 import api_router


# --- Definir el ciclo de vida (Lifespan) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Maneja el inicio y cierre de la aplicación"""
    # Lógica de Startup (antes de que la app reciba peticiones)
    print("📦 Verificando base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas/verificadas correctamente")
    
    yield  # Aquí es donde la app funciona 
    
    # Lógica de Shutdown (cuando la app se detiene, si fuera necesario)
    print("🛑 Apagando SmartGym API...")

# --- Crear la aplicación FastAPI ---
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API para gestión integral de SmartGym - Laboratorio I",
    docs_url="/docs",     # Swagger UI
    redoc_url="/redoc",   # ReDoc (documentación alternativa)
    lifespan=lifespan
)

# --- Configurar CORS (para futuros frontends) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Incluir todos los routers  ---
app.include_router(api_router, prefix="/api/v1")

# --- Endpoint raíz ---
@app.get("/")
def root():
    """Endpoint de bienvenida y verificación de estado"""
    return {
        "aplicacion": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "estado": "🟢 Operativa",
        "documentacion": "/docs",
        "base_datos": "PostgreSQL"
    }


# --- Endpoint de health check ---
@app.get("/health")
def health_check():
    """Endpoint para verificar que la API está viva"""
    return {
        "status": "healthy",
        "database": "connected",
        "TEAM":"Escuadron Mete La Pata :)"
    }

from app.core.dependencies import get_current_user
from app.models.usuario import Usuario
from fastapi import Depends
from sqlalchemy.orm import Session
from app.models.database import get_db


@app.get("/test-auth")
def test_auth(current_user: Usuario = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "rol": current_user.rol.nombre}

@app.get("/test-disciplinas")
def test_disciplinas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    print(f"🔍 TEST DISCIPLINAS - Usuario: {current_user.email}")
    return {"msg": "ok"}