# ArmorTrack - Sistema de Control e Incautación de Vehículos

**ArmorTrack** es una solución de software de escritorio robusta y profesional diseñada para la gestión, registro, control e incautación de vehículos y motocicletas. El sistema fue desarrollado para responder a una **necesidad crítica de control de inventarios dentro de una Comisaría**, la cual no contaba con una herramienta digital estructurada para supervisar los bienes retenidos, depositados o incautados. 

Pensando en el flujo operativo del día a día policial, ArmorTrack sustituye los registros manuales por una plataforma digital centralizada, ágil y de manejo jerárquico que garantiza la integridad, trazabilidad y transparencia en la custodia de los vehículos.

Construido bajo una arquitectura modular, cuenta con una interfaz gráfica intuitiva inspirada en los lineamientos visuales de macOS, ofreciendo una experiencia reactiva y fluida para el operador.

---

## ⚠️ Estado del Proyecto y Próximas Funciones

El sistema se encuentra actualmente en **fase de prueba y desarrollo activo**. Aunque los módulos principales de registro y visualización son completamente funcionales, todavía se están diseñando e implementando características críticas para su despliegue final.

### 🗺️ Mapa de Ruta (Pendientes de Implementación)
*   **Impresión del Acta de Entrega**: Generación automatizada y exportación de documentos oficiales en formato físico o PDF para la devolución de los bienes.
*   **Módulo de Registro de Usuarios**: Panel administrativo para dar de alta nuevos operadores y asignar credenciales de forma controlada.
*   **Edición de Datos Cargados**: Posibilidad de modificar o corregir registros ya guardados en el histórico (con auditoría de roles).
*   *Y muchas funciones más en planificación para optimizar el entorno operativo de la comisaría.*

---

## 🏗️ Arquitectura del Sistema

El proyecto sigue una estructura limpia basada en la separación de responsabilidades, dividiendo claramente la interfaz de usuario de la capa lógica y el almacenamiento persistente:

*   **`Presentation/`**: Capa de interfaz gráfica basada en `customtkinter`. Implementa formularios dinámicos, paneles de reportes expansibles y flujos de navegación estructurados.
*   **`Logic/`**: Centraliza las reglas de negocio, validaciones de datos y tratamiento de la información antes de su persistencia (`InventarioLogica`, `Autenticador`).
*   **`Database/`**: Repositorio de datos. Utiliza archivos `.json` para catálogos dinámicos (marcas/modelos) y un motor relacional en **SQLite3** (`inventario.db`) para garantizar la integridad de los datos estructurados en caliente.

---

## 🎯 Componentes y Funcionalidades Desarrolladas

### 1. Sistema de Autenticación y Control de Acceso
*   Validación y control de sesiones mediante procesamiento estructurado.
*   Asignación interna de roles (`rol_actual`) para la jerarquización de permisos.

### 2. Formulario Inteligente de Registro e Incautación (`FormularioVehiculo`)
*   **UI Reactiva**: Oculta y muestra campos en tiempo real según el tipo de vehículo (`VEHÍCULO` o `MOTOCICLETA`).
*   **Campos de Extensión Dinámica**: Si un elemento no figura en el catálogo precargado, permite la inyección automática de entradas de texto manuales ("OTRO...") sin interrumpir el flujo.

### 3. Panel de Reportes e Inventario Avanzado (`VentanaReportes`)
*   **Métricas en Caliente**: Estadísticas en tiempo real mediante consultas optimizadas `COUNT(*)` en SQLite.
*   **Tarjetas Colapsables**: Renderizado interactivo de registros que expande detalles técnicos adicionales (Unidad a cargo, observaciones, leyes aplicadas, etc.) al hacer clic.

---

## 🛠️ Stack Tecnológico

*   **Lenguaje**: Python 3.10+
*   **Interfaz Gráfica**: `customtkinter` (Modo Oscuro nativo)
*   **Manipulación de Imágenes**: `Pillow` (Tratamiento de logos institucionales)
*   **Base de Datos Relacional**: `sqlite3` (Conexiones optimizadas con administradores de contexto `with`)

---

## 💻 Instalación y Despliegue

1. Clonar el repositorio.
2. Instalar las dependencias requeridas:
   ```bash
   pip install customtkinter pillow