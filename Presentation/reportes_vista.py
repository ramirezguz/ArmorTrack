import customtkinter as ctk

class VentanaReportes(ctk.CTkFrame):
    def __init__(self, parent, registro_logica=None):
        super().__init__(parent, fg_color="transparent")
        self.parent = parent
        self.logica = registro_logica
        
        self.font_title = ("SF Pro Display", 20, "bold")
        self.font_subtitle = ("SF Pro Text", 13, "bold")
        self.font_body = ("SF Pro Text", 12)
        
        self.lbl_titulo = ctk.CTkLabel(self, text="📊 PANEL DE REPORTES E INVENTARIO", font=self.font_title)
        self.lbl_titulo.pack(pady=(10, 15))
        
        self.frame_stats = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_stats.pack(fill="x", pady=5)
        
        self.lbl_total_val = ctk.CTkLabel(self.frame_stats, text="📋 Total: 0", font=self.font_subtitle, text_color="#3A9FBF")
        self.lbl_total_val.pack(side="left", padx=20)
        
        self.lbl_vehiculos_val = ctk.CTkLabel(self.frame_stats, text="🚗 Automotores: 0", font=self.font_subtitle, text_color="#2ECC71")
        self.lbl_vehiculos_val.pack(side="left", padx=20)
        
        self.lbl_motos_val = ctk.CTkLabel(self.frame_stats, text="🏍️ Motocicletas: 0", font=self.font_subtitle, text_color="#E67E22")
        self.lbl_motos_val.pack(side="left", padx=20)
        
        self.frame_busqueda = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_busqueda.pack(fill="x", padx=20, pady=5)

        self.txt_buscar = ctk.CTkEntry(
            self.frame_busqueda, placeholder_text="Buscar por Matrícula, Chasis, Marca, Conductor o Fiscalía...", 
            font=self.font_body, height=40, fg_color="#1E1E1E", border_color="#3A3A3A"
        )
        self.txt_buscar.pack(side="left", fill="x", expand=True, padx=(0, 12))
        self.txt_buscar.bind("<Return>", lambda e: self.actualizar_reporte())

        self.btn_buscar = ctk.CTkButton(
            self.frame_busqueda, text="🔍 Filtrar", font=self.font_subtitle,
            width=120, height=40, fg_color="#007AFF", command=self.actualizar_reporte
        )
        self.btn_buscar.pack(side="right")

        self.tabla_container = ctk.CTkScrollableFrame(
            self, fg_color="#1E1E1E", corner_radius=12, border_width=1, border_color="#333333"
        )
        self.tabla_container.pack(fill="both", expand=True, padx=20, pady=15)

        self.actualizar_reporte()

    def actualizar_reporte(self):
        """Actualiza las metricas globales y regenera las filas del listado según los criterios de búsqueda."""
        for widget in self.tabla_container.winfo_children():
            widget.destroy()

        if self.logica and hasattr(self.logica, "obtener_estadisticas_totales"):
            stats = self.logica.obtener_estadisticas_totales()
            self.lbl_total_val.configure(text=f"📋 Total: {stats.get('total', 0)}")
            self.lbl_vehiculos_val.configure(text=f"🚗 Automotores: {stats.get('vehiculos', 0)}")
            self.lbl_motos_val.configure(text=f"🏍️ Motocicletas: {stats.get('motos', 0)}")
        
        criterio = self.txt_buscar.get().strip()
        resultados = self.logica.buscar_vehiculos(criterio) if self.logica and hasattr(self.logica, "buscar_vehiculos") else []

        if not resultados:
            lbl_vacio = ctk.CTkLabel(
                self.tabla_container, text="⚠️ No hay registros que coincidan con la búsqueda.", 
                font=self.font_body, text_color="#8E8E93"
            )
            lbl_vacio.pack(pady=40)
            return

        for vehiculo in resultados:
            card_item = ctk.CTkFrame(self.tabla_container, fg_color="#262626", corner_radius=8, border_width=1, border_color="#3A3A3A")
            card_item.pack(fill="x", padx=10, pady=6)
            card_item.configure(cursor="hand2")

            info_basica_frame = ctk.CTkFrame(card_item, fg_color="transparent")
            info_basica_frame.pack(fill="x", padx=12, pady=8)

            tipo_txt = f"【 {vehiculo.get('tipo', 'VEHÍCULO')} 】 - {vehiculo.get('subcategoria', 'N/A')} — ESTADO: {vehiculo.get('estado', 'N/A')}"
            info_principal = f"{vehiculo.get('marca', 'S/M')} {vehiculo.get('modelo', 'S/M')} – Color: {vehiculo.get('color', 'S/C')} – Año: {vehiculo.get('ano_vehiculo', 'N/A')}"
            datos_identificacion = f"Chapa/Matrícula: {vehiculo.get('Matricula') or vehiculo.get('matricula') or 'SIN MATRÍCULA'}  |  N° de Chasis: {vehiculo.get('chasis', 'SIN CHASIS')}"
            conductor_txt = f"👤 Conductor: {vehiculo.get('nombre_conductor', 'DESCONOCIDO')} (C.I.: {vehiculo.get('ci_conductor', 'N/A')})"

            lbl_tipo = ctk.CTkLabel(info_basica_frame, text=tipo_txt, font=ctk.CTkFont(size=11, weight="bold"), text_color="#3A9FBF")
            lbl_tipo.pack(anchor="w")
            
            lbl_prin = ctk.CTkLabel(info_basica_frame, text=info_principal, font=ctk.CTkFont(size=14, weight="bold"), text_color="#FFFFFF")
            lbl_prin.pack(anchor="w", pady=(2, 4))
            
            lbl_ident = ctk.CTkLabel(info_basica_frame, text=datos_identificacion, font=ctk.CTkFont(size=12), text_color="#2ECC71")
            lbl_ident.pack(anchor="w")
            
            lbl_cond = ctk.CTkLabel(info_basica_frame, text=conductor_txt, font=ctk.CTkFont(size=11), text_color="#AAAAAA")
            lbl_cond.pack(anchor="w", pady=(2, 0))

            detalles_extras_frame = ctk.CTkFrame(card_item, fg_color="#1E1E1E", corner_radius=6)
            
            extras_txt = (
                f"• ID Registro Interno: #{vehiculo.get('id', 'S/N')}\n"
                f"• Inscripto a Nombre de: {vehiculo.get('Inscripto a Nombre de') or vehiculo.get('inscripto_nombre') or 'NO REGISTRA'}\n"
                f"• Cedula de Idenitdad N°: {vehiculo.get('C_I_N°') or vehiculo.get('ci_num') or 'N/A'}\n"
                f"• Fecha de Incautacion: {vehiculo.get('fecha_incautacion', 'S/D')}\n"
                f"• Unidad Fiscal Interviniente: {vehiculo.get('unidad_a_cargo', 'NINGUNA')}\n"
                f"• Fiscal Interviniente: {vehiculo.get('fiscal_a_cargo', 'A DETERMINAR')}\n"
                f"• Causa o Motivo de Incautacion: {vehiculo.get('causa_incautacion') or vehiculo.get('observacion') or 'Sin observaciones.'}"
            )
            
            lbl_extras = ctk.CTkLabel(
                detalles_extras_frame, text=extras_txt, font=ctk.CTkFont(size=12), text_color="#DDDDDD",
                justify="left", anchor="w", wraplength=650
            )
            lbl_extras.pack(fill="x", padx=15, pady=10)

            def alternar_tarjeta(event, frame_oculto=detalles_extras_frame):
                if frame_oculto.winfo_viewable():
                    frame_oculto.pack_forget()
                else:
                    frame_oculto.pack(fill="x", padx=12, pady=(0, 10))

            card_item.bind("<Button-1>", alternar_tarjeta)
            info_basica_frame.bind("<Button-1>", alternar_tarjeta)
            lbl_tipo.bind("<Button-1>", alternar_tarjeta)
            lbl_prin.bind("<Button-1>", alternar_tarjeta)
            lbl_ident.bind("<Button-1>", alternar_tarjeta)
            lbl_cond.bind("<Button-1>", alternar_tarjeta)