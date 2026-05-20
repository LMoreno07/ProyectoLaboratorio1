
# 🏋️ SmartGym API

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-✓-2496ED?logo=docker)
![Swagger](https://img.shields.io/badge/Swagger-✓-85EA2D?logo=swagger)

API RESTful para la gestión integral del gimnasio SmartGym. Centraliza operaciones administrativas, financieras y deportivas con control de acceso, membresías, reservas de clases y punto de venta.

---

## 📑 Tabla de Contenidos

- [Características](#-características)
- [Stack Tecnológico](#-stack-tecnológico)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Documentación API](#-documentación-api)
- [Autores](#-autores)

---

## ✨ Características

- 🔐 **Autenticación JWT**: Login seguro con tokens Bearer
- 👥 **Roles y permisos**: Admin, Finanzas, Entrenador, Cliente
- 🏋️ **Gestión deportiva**: Disciplinas, sesiones, reservas con control de cupos
- 💳 **Membresías y pagos**: Planes de suscripción, pagos inmutables
- 🔧 **Inventario**: Máquinas, mantenimiento preventivo/correctivo
- 🛒 **Punto de venta**: Productos, stock, transacciones
- 📊 **Seguimiento biométrico**: Evolución física de clientes
- 🚪 **Control de acceso**: Validación de membresía por cédula
- 📖 **Swagger autogenerado**: Documentación interactiva OpenAPI
- 🐳 **Dockerizado**: Despliegue con un solo comando

---

## 🛠️ Stack Tecnológico

| Herramienta | Propósito |
|-------------|-----------|
| **Python 3.12** | Lenguaje principal |
| **FastAPI** | Framework web asíncrono |
| **PostgreSQL 16** | Base de datos relacional |
| **SQLAlchemy 2.0** | ORM para acceso a datos |
| **Alembic** | Migraciones de base de datos |
| **Pydantic** | Validación de esquemas |
| **JWT (python-jose)** | Autenticación |
| **bcrypt (passlib)** | Hasheo de contraseñas |
| **Docker + Compose** | Contenerización y orquestación |
| **Swagger/OpenAPI** | Documentación interactiva |

---

## 📋 Requisitos Previos

- [Docker](https://www.docker.com/products/docker-desktop/) (v24+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.23+)
- [Git](https://git-scm.com/downloads) (opcional)

> **Nota:** No necesitas Python ni PostgreSQL instalados. Docker lo maneja todo.

---

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio

```bash

git clone https://github.com/TU-USUARIO/smartgym-api.git

git clone https://github.com/LMoreno07/ProyectoLaboratorio1.git
git clone https://github.com/TU-USUARIO/smartgym-api.git
cd smartgym-api
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
nano .env
```

### 3. Levantar los servicios

```bash
docker-compose up -d
```

### 4. Verificar que todo funciona

```bash
docker-compose logs api
docker-compose logs db
```

---

🎯 Uso

Acceder a la documentación interactiva

· Swagger UI: http://localhost:8000/docs
· ReDoc: http://localhost:8000/redoc

Probar la API con datos de ejemplo

```bash
# 1. Crear roles
curl -X POST http://localhost:8000/api/v1/roles/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Administrador"}'

# 2. Crear usuario administrador
curl -X POST http://localhost:8000/api/v1/usuarios/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@smartgym.com", "password": "Admin123!", "nombre": "Admin", "apellido": "Sistema", "rol_id": 1}'

# 3. Listar usuarios
curl http://localhost:8000/api/v1/usuarios/
```

Comandos útiles

```bash
docker-compose down              # Detener servicios
docker-compose down -v           # Detener y eliminar datos
docker-compose build --no-cache  # Reconstruir imágenes
docker-compose logs -f api       # Ver logs en tiempo real
docker-compose exec api alembic upgrade head              # Ejecutar migraciones
docker-compose exec api alembic revision --autogenerate -m "descripcion"  # Crear migración
```

---

📁 Estructura del Proyecto

```
smartgym-api/
├── app/                        # Código fuente de la API
│   ├── api/v1/                 # Endpoints versionados
│   │   └── endpoints/          # Un archivo por módulo
│   ├── core/                   # Configuración, seguridad, dependencias
│   ├── models/                 # Modelos ORM (SQLAlchemy)
│   ├── schemas/                # Esquemas de validación (Pydantic)
│   ├── services/               # Lógica de negocio
│   ├── utils/                  # Utilidades
│   └── main.py                 # Punto de entrada
├── migrations/                 # Migraciones de base de datos (Alembic)
│   ├── versions/               # Archivos de migración
│   └── env.py                  # Configuración de Alembic
├── .env.example                # Plantilla de variables de entorno
├── .gitattributes              # Configuración de Git
├── .gitignore                  # Archivos ignorados por Git
├── alembic.ini                 # Configuración de Alembic
├── docker-compose.yml          # Orquestación de servicios
├── Dockerfile                  # Imagen de la API
└── requirements.txt            # Dependencias Python
```

---

📖 Documentación API

Recurso URL
Swagger UI http://localhost:8000/docs
ReDoc http://localhost:8000/redoc
OpenAPI JSON http://localhost:8000/openapi.json

---

👥 Autores

Nombre
Luis Moreno 
Adrián Ortegano 
Isaias Tovar 

Universidad Centroccidental "Lisandro Alvarado" (UCLA)
Laboratorio I - Lapso 2026-1
Profesor: Jonathan Falcon

---

📄 Licencia

Este proyecto es parte de una actividad académica de la UCLA. Todos los derechos reservados © 2026.
