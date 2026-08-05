import customtkinter as ctk


class VentanaReportes(ctk.CTkFrame):
    def __init__(self, parent, logica_reportes=None):
        super().__init__(parent, fg_color="transparent")
        self.parent = parent
        self.logica = logica_reportes

        # Configuración de la cuadrícula principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.crear_componentes()

    def crear_componentes(self):
        # --- 1. PANEL SUPERIOR DE FILTROS ---
        frame_filtros = ctk.CTkFrame(self)
        frame_filtros.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        lbl_titulo = ctk.CTkLabel(
            frame_filtros,
            text="Reporte y Consulta de Vehículos",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        lbl_titulo.pack(side="left", padx=15, pady=15)

        lbl_estado = ctk.CTkLabel(frame_filtros, text="Estado:")
        lbl_estado.pack(side="left", padx=(20, 5), pady=15)

        # 1. Definimos combo_filtro_estado AQUÍ antes de llamar a cargar_tabla_reporte
        self.combo_filtro_estado = ctk.CTkOptionMenu(
            frame_filtros,
            values=["TODOS", "INCAUTADO", "DEPOSITADO", "ENTREGADO"],
            command=lambda choice: self.cargar_tabla_reporte()
        )
        self.combo_filtro_estado.pack(side="left", padx=5, pady=15)
        self.combo_filtro_estado.set("TODOS")

        btn_refrescar = ctk.CTkButton(
            frame_filtros,
            text="Filtrar / Actualizar",
            command=self.cargar_tabla_reporte
        )
        btn_refrescar.pack(side="left", padx=15, pady=15)

        # --- 2. TABLA CON CTKSCROLLABLEFRAME ---
        self.frame_tabla = ctk.CTkFrame(self)
        self.frame_tabla.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.frame_tabla.grid_columnconfigure(0, weight=1)
        self.frame_tabla.grid_rowconfigure(1, weight=1)

        # Encabezados de la tabla
        frame_encabezados = ctk.CTkFrame(self.frame_tabla, fg_color=("gray85", "gray25"))
        frame_encabezados.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        
        columnas = ["N° Chasis / Dominio", "Marca", "Modelo", "Tipo", "Estado", "Fecha Ingreso"]
        for i, col in enumerate(columnas):
            frame_encabezados.grid_columnconfigure(i, weight=1)
            lbl_col = ctk.CTkLabel(frame_encabezados, text=col, font=ctk.CTkFont(weight="bold"))
            lbl_col.grid(row=0, column=i, padx=5, pady=8)

        # Contenedor scrolleable para las filas de datos
        self.scroll_datos = ctk.CTkScrollableFrame(self.frame_tabla, fg_color="transparent")
        self.scroll_datos.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        for i in range(len(columnas)):
            self.scroll_datos.grid_columnconfigure(i, weight=1)

        # --- 3. CARGAMOS LOS DATOS EN LA TABLA ---
        self.cargar_tabla_reporte()

    def cargar_tabla_reporte(self):
        # Verificación de seguridad por si el atributo aún no fue instanciado
        if not hasattr(self, "combo_filtro_estado"):
            return

        estado_filtrar = self.combo_filtro_estado.get()

        # Limpiar filas existentes en el marco scrolleable
        for child in self.scroll_datos.winfo_children():
            child.destroy()

        # Obtención de registros (desde la lógica o estáticos para pruebas), de momento estaticos, para prueba
        registros = []
        if self.logica and hasattr(self.logica, "obtener_vehiculos"):
            registros = self.logica.obtener_vehiculos(estado_filtrar)
        else:
            registros = [
                ("123456789", "Toyota", "Hilux", "Vehículo", "INCAUTADO", "2026-04-01"),
                ("987654321", "Kenton", "GTR 150", "Motocicleta", "DEPOSITADO", "2026-04-02"),
                ("456789123", "Honda", "Civic", "Vehículo", "ENTREGADO", "2026-04-03"),
            ]

        # Insertar filas filtradas utilizando componentes nativos de CustomTkinter
        fila_idx = 0
        for reg in registros:
            # Si es "TODOS" o coincide el estado (reg[4])
            if estado_filtrar == "TODOS" or reg[4] == estado_filtrar:
                # Fondo alternado para lectura cómoda de filas
                color_fondo = ("gray90", "gray20") if fila_idx % 2 == 0 else "transparent"
                
                row_frame = ctk.CTkFrame(self.scroll_datos, fg_color=color_fondo)
                row_frame.pack(fill="x", pady=2)

                for col_idx, dato in enumerate(reg):
                    row_frame.grid_columnconfigure(col_idx, weight=1)
                    lbl_dato = ctk.CTkLabel(row_frame, text=str(dato))
                    lbl_dato.grid(row=0, column=col_idx, padx=5, pady=5)

                fila_idx += 1