# ArmorTrack - Sistema de Control e Incautación de Vehículos

**ArmorTrack** es una solución de software integral y profesional diseñada para la gestión, registro, control e incautación de vehículos y motocicletas. El sistema fue desarrollado para responder a una **necesidad crítica de control de inventarios dentro de una Comisaría**, la cual no contaba con una herramienta digital estructurada para supervisar los bienes retenidos, depositados, incautados o entregados.

Pensando en el flujo operativo del día a día policial, ArmorTrack sustituye los registros manuales por una plataforma centralizada, ágil y reactiva que garantiza la integridad, trazabilidad y transparencia en la custodia de los vehículos.

Actualmente, ArmorTrack evoluciona hacia una **arquitectura cliente-servidor moderna** compuesta por una API RESTful en **FastAPI** y una interfaz web reactiva desarrollada en **React (Vite)**, manteniendo además la compatibilidad con el cliente de escritorio en **CustomTkinter**.

---

## 🚀 Novedades y Últimos Avances

- **Módulo Web React + Vite**: Implementación del nuevo panel web interactivo para la gestión centralizada de registros, entregas y reportes.
- **Backend API REST (FastAPI + SQLAlchemy)**: Creación de endpoints optimizados para consultar estadísticas globales y realizar búsquedas complejas en tiempo real.
- **Filtro Avanzado por Estado en Reportes**: 
  - Capacidad de filtrar el inventario por estado exacto: **Retenido / Incautado**, **Depositado** y **Entregado**.
  - Búsqueda combinada por texto (Matrícula, Chasis, Marca, Conductor, Fiscalía, Causa).
  - Integración de filtrado dinámico en frontend y soporte de parámetros Query (`criterio` y `estado`) en el backend.
- **Soporte de CORS**: Configuración de middleware para permitir una comunicación fluida y segura entre la SPA (Single Page Application) de React y la API de FastAPI.

---

## 🗺️ Mapa de Ruta (Próximos Pasos)

* **Impresión de Actas Oficiales**: Generación y exportación automatizada de Actas de Entrega / Incautación en formato PDF para firma física o digital.
* **Gestión de Usuarios y Permisos**: Autenticación JWT y control de acceso basado en roles (`ADMIN`, `OPERADOR`).
* **Edición y Auditoría de Históricos**: Modificación controlada de registros existentes con registro de auditoría de modificaciones.

---

## 🏗️ Arquitectura del Sistema

El proyecto sigue una estructura limpia, modular y desacoplada dividida en capas:

```text
ArmorTrack/
├── Database/              # Modelos SQLAlchemy, scripts de inicialización y SQLite
│   ├── init_db.py
│   └── models.py
├── Logic/                 # Lógica de negocio y reglas del inventario / salidas
│   ├── logica_inventario.py
│   └── salida_vehiculo.py
├── Presentation/          # Interfaz gráfica de escritorio (CustomTkinter)
│   ├── formulario_vehiculo.py
│   └── reportes_vista.py
├── frontend/              # Aplicación Web (React + Vite)
│   ├── src/
│   │   ├── component/
│   │   │   ├── VistaRegistro.jsx
│   │   │   ├── VistaEntrega.jsx
│   │   │   └── VistaReportes.jsx
│   │   └── App.jsx
└── main.py                # Servidor Backend FastAPI (API REST)
```

---

## 🎯 Componentes y Funcionalidades Principales

### 1. Panel de Reportes e Inventario Avanzado (`VistaReportes`)
* **Métricas Globales**: Visualización en tiempo real del Total de Registros, Automotores y Motocicletas.
* **Filtros Combinados**: Selector desplegable por estado (*Todos*, *Retenido/Incautado*, *Depositado*, *Entregado*) interactivo y reactivo.
* **Tarjetas Interactivas**: Tarjetas desplegables que exponen los detalles judiciales e identificación técnica (Unidad Fiscal, Fiscal interviniente, Causa, Inscripto, etc.).

### 2. Formulario de Registro e Incautación
* **UI Dinámica**: Selección adaptable de campos según tipo de vehículo (`VEHÍCULO` o `MOTOCICLETA`).
* **Ingreso de Marcas/Modelos**: Posibilidad de seleccionar de catálogos o inyectar nuevos registros de forma transparente.

### 3. API RESTful
* `GET /api/v1/estadisticas`: Retorna métricas globales consolidadas.
* `GET /api/v1/vehiculos/buscar`: Búsqueda flexible multicriterio con filtrado opcional por estado.

---

## 🛠️ Stack Tecnológico

* **Backend**: Python 3.10+, FastAPI, Uvicorn, SQLAlchemy, Pydantic.
* **Frontend Web**: React 18, Vite, JavaScript (ES6+), CSS3 / Inline Styling.
* **Desktop Client**: CustomTkinter, Pillow.
* **Base de Datos**: SQLite3.

---

## 💻 Instalación y Despliegue Local

### 1. Clonar el Repositorio
```bash
git clone https://github.com/ramirezguz/ArmorTrack.git
cd ArmorTrack
```

### 2. Configurar y Ejecutar el Backend (FastAPI)
```bash
# Crear y activar entorno virtual
python -m venv venv

# En Windows:
venv\Scripts\activate
# En Linux/macOS:
source venv/bin/activate

# Instalar dependencias backend
pip install fastapi uvicorn sqlalchemy customtkinter pillow pydantic

# Iniciar servidor FastAPI
uvicorn main:app --reload
```
*El servidor backend quedará corriendo en `http://127.0.0.1:8000`.*

### 3. Configurar y Ejecutar el Frontend (React + Vite)
```bash
cd frontend
npm install
npm run dev