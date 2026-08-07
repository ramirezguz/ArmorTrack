# ArmorTrack - Sistema de Control e Incautación de Vehículos

**ArmorTrack** es una aplicación de escritorio diseñada para la gestión, registro, control e incautación de vehículos y motocicletas. Construida bajo una arquitectura modular y una interfaz gráfica inspirada en los lineamientos visuales de macOS, la plataforma ofrece una experiencia de usuario fluida, robusta y con alta reactividad de componentes nativos.

---

## 🏗️ Arquitectura del Sistema

El proyecto sigue una estructura limpia inspirada en la separación de responsabilidades, dividiendo claramente la interfaz de usuario de la capa lógica y el almacenamiento persistente:

*   **`Presentation/`**: Contiene la capa de interfaz gráfica basada en `customtkinter`. Implementa formularios dinámicos, paneles de reportes expansibles, alertas modales personalizadas y flujos de navegación estructurados.
*   **`Logic/`**: Alberga las reglas de negocio del sistema (`InventarioLogica`, `Autenticador`, `RegistroEntrada`). Centraliza las validaciones de datos, la gestión de sesiones y el tratamiento de la información antes de su persistencia.
*   **`Database/`**: Repositorio de datos estructurados. Utiliza archivos dinámicos `.json` para la precarga en memoria de catálogos (marcas y modelos) y un motor relacional en **SQLite3** (`inventario.db`) para garantizar transaccionalidad e integridad de datos en caliente.

---

## 🎯 Componentes y Funcionalidades Desarrolladas

### 1. Sistema de Autenticación y Control de Acceso (`VentanaLogin`, `Autenticador`)
*   Interfaz de inicio de sesión compacta y minimalista.
*   Carga y validación en caliente mediante el procesamiento estructurado de `usuarios.json`.
*   Asignación interna de roles (`rol_actual`) para la futura implementación de permisos jerárquicos.

### 2. Panel Principal Dynamic Sidebar (`VentanaMenuPrincipal`, `App`)
*   Arquitectura de marco contenedor único (`container`) que intercambia vistas dinámicamente destruyendo e instanciando sub-frames sin pérdida de memoria.
*   Barra de navegación lateral fija (`sidebar`) con ajuste adaptativo de geometrías (de `450x550` para autenticación a `1000x650` escalable para el área de trabajo).

### 3. Formulario Inteligente de Registro e Incautación (`FormularioVehiculo`)
*   **Carga Asíncrona simulada/JSON**: Dependiendo del tipo (`VEHÍCULO` o `MOTOCICLETA`), lee en tiempo de ejecución las bases de datos de marcas y modelos correspondientes (`vehiculos.json` / `motocicletas.json`).
*   **UI Reactiva / Grid Dinámico**: Oculta y muestra campos en tiempo real (ej. *Subcategoría / Carrocería* solo visible para vehículos).
*   **Campos de Extensión Manual ("OTRO...")**: Si una marca, modelo o subcategoría no figura en el catálogo precargado, el formulario inyecta dinámicamente un campo de entrada de texto (`CTkEntry`) con auto-focus para no detener el flujo de trabajo del operador.
*   **Control del Grid Nativo**: Solución avanzada ante solapamientos empleando `grid_forget()` y reasignación explícita de filas intermedias.

### 4. Panel de Reportes e Inventario Avanzado (`VentanaReportes`)
*   **Métricas en Caliente**: Consulta sincrónica agregada mediante consultas `COUNT(*)` optimizadas en la base de datos SQLite.
*   **Buscador Indexado**: Filtrado a través del evento `<Return>` o botón de acción, ejecutando búsquedas con operadores parciales `LIKE` sobre matrículas o números de chasis.
*   **Tarjetas Colapsables Interactivas**: Cada registro renderiza una tarjeta resumen. Al hacer clic (`<Button-1>`), se expande un panel interno con detalles técnicos adicionales (Número de registro interno, Año de incautación, Unidad a cargo, Leyes aplicadas/Observaciones).

---

## 🛠️ Stack Tecnológico

*   **Lenguaje**: Python 3.10+
*   **Interfaz Gráfica**: `customtkinter` (Modo Oscuro nativo, temas basados en Apple SF Pro Display / Text).
*   **Manipulación de Imágenes**: `Pillow` (`PIL.Image` para el tratamiento adaptativo de logos corporativos).
*   **Base de Datos Relacional**: `sqlite3` (Conexiones optimizadas por contexto empleando administradores de contexto `with` y mapeo relacional mediante `sqlite3.Row`).
*   **Intercambio de Datos**: `json` (Formatos UTF-8 estructurados).

---

## 🚀 Hoja de Ruta: Próximas Implementaciones (En Desarrollo)

El sistema ha sido estructurado siguiendo principios OCP (Open/Closed Principle) para facilitar la integración de las siguientes funcionalidades planificadas:

### 📋 Módulo Completo de Salida / Entrega de Vehículos
*   *Estado Actual*: Estructurado visualmente a través del botón `📋 Entregar Vehículo` en el menú principal.
*   *Desarrollo Pendiente*: Formulario de validación de liberación. Requerirá la verificación de órdenes judiciales, registro de datos de la persona que retira (C.I., Parentesco, Rol) y cambio de estado automatizado en la base de datos a `ENTREGADO`.

### 🔐 Capa de Seguridad y Criptografía en Autenticación
*   *Estado Actual*: Validación de texto plano sobre `usuarios.json`.
*   *Desarrollo Pendiente*: Implementación de hashing salteado (`bcrypt` o `hashlib.pbkdf2_hmac`) para el almacenamiento seguro de credenciales.

### 📜 Auditoría e Historial de Modificaciones
*   *Estado Actual*: Base de datos guarda registros únicos.
*   *Desarrollo Pendiente*: Creación de una tabla `logs_auditoria` en SQLite para almacenar qué usuario realizó un registro, qué modificaciones sufrió una ficha técnica y la marca de tiempo exacta (`TIMESTAMP`).

### 📊 Exportación de Reportes Multiformato
*   *Estado Actual*: Consulta visual en pantalla.
*   *Desarrollo Pendiente*: Botón de acción en el Panel de Reportes para exportar los inventarios actuales filtrados a archivos tabulares **Excel (.xlsx)** y actas oficiales de incautación en formato **PDF** de forma local.

---

## 💻 Instalación y Despliegue

1. Clonar el repositorio.
2. Asegurar la instalación de las dependencias requeridas:
   ```bash
   pip install customtkinter pillow
   ```
3. Ejecutar el punto de entrada principal del sistema:
   ```bash
   python main.py
   ```
