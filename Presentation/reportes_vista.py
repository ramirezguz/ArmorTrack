import customtkinter as ctk

class VentanaReportes(ctk.CTkFrame):
    def __init__(self, parent, registro_logica=None):
        super().__init__(parent, fg_color="transparent")
        self.parent = parent
        self.logica = registro_logica
        
        self.font_title = ("SF Pro Display", 20, "bold")
        self.font_subtitle = ("SF Pro Text", 13, "bold")
        self.font_body = ("SF Pro Text", 12)
        
        # # 1. Título
        self.lbl_titulo = ctk.CTkLabel(self, text="📊 PANEL DE REPORTES E INVENTARIO", font=self.font_title)
        self.lbl_titulo.pack(pady=(10, 15))
        
        # # 2. (Resumen rápido arriba) 
        self.frame_stats = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_stats.pack(fill="x", pady=5)
        
        self.lbl_total_val = ctk.CTkLabel(self.frame_stats, text="Total: 0", font=self.font_subtitle, text_color="#3A9FBF")
        self.lbl_total_val.pack(side="left", padx=20)
        
        self.lbl_vehiculos_val = ctk.CTkLabel(self.frame_stats, text="Vehículos: 0", font=self.font_subtitle, text_color="#2ECC71")
        self.lbl_vehiculos_val.pack(side="left", padx=20)
        
        self.lbl_motos_val = ctk.CTkLabel(self.frame_stats, text="Motos: 0", font=self.font_subtitle, text_color="#E67E22")
        self.lbl_motos_val.pack(side="left", padx=20)
        
        self.filtrar_vehiculos()

    def filtrar_vehiculos(self): # O el nombre que tenga tu función de filtrado
    # 1. Consultar estadísticas a la base de datos
        if self.logica and hasattr(self.logica, "obtener_estadisticas_totales"):
            stats = self.logica.obtener_estadisticas_totales()
        else:
            stats = {"total": 0, "vehiculos": 0, "motos": 0}

        self.lbl_total_val.configure(text=f"Total: {stats['total']}")
        self.lbl_vehiculos_val.configure(text=f"Vehículos: {stats['vehiculos']}")
        self.lbl_motos_val.configure(text=f"Motos: {stats['motos']}")

        # 3. Buscador
        self.frame_busqueda = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_busqueda.pack(fill="x", padx=20, pady=5)

        self.txt_buscar = ctk.CTkEntry(
            self.frame_busqueda, 
            placeholder_text="Buscar por Matrícula, Chasis, Marca o Propietario...", 
            font=self.font_body,
            height=40,
            fg_color="#1E1E1E",
            border_color="#3A3A3A"
        )
        self.txt_buscar.pack(side="left", fill="x", expand=True, padx=(0, 12))
        self.txt_buscar.bind("<Return>", lambda e: self.actualizar_reporte())

        self.btn_buscar = ctk.CTkButton(
            self.frame_busqueda, 
            text="🔍 Filtrar", 
            font=self.font_subtitle,
            width=120, 
            height=40, 
            fg_color="#007AFF",
            command=self.actualizar_reporte
        )
        self.btn_buscar.pack(side="right")

        # 4. Contenedor de datos
        self.tabla_container = ctk.CTkScrollableFrame(
            self, 
            fg_color="#1E1E1E", 
            corner_radius=12,
            border_width=1,
            border_color="#333333"
        )
        self.tabla_container.pack(fill="both", expand=True, padx=20, pady=15)

        # Cargar los datos la primera vez
        self.actualizar_reporte()

    def actualizar_reporte(self):
        """Limpia el visor, actualiza las métricas y dibuja las tarjetas filtradas."""
        # A. Limpiar la tabla visual
        for widget in self.tabla_container.winfo_children():
            widget.destroy()

        # B. Actualizar tarjetas informativas superiores
        if self.logica and hasattr(self.logica, "obtener_metricas_resumen"):
            stats = self.logica.obtener_metricas_resumen()
            self.lbl_total_val.configure(text=f"📋 Total Incautados: {stats['total_general']}")
            self.lbl_autos_val.configure(text=f"🚗 Automotores: {stats['total_vehiculos']}")
            self.lbl_motos_val.configure(text=f"🏍️ Motocicletas: {stats['total_motocicletas']}")
        
        # C. Consultar los datos filtrados a la lógica
        criterio = self.txt_buscar.get()
        if self.logica and hasattr(self.logica, "buscar_vehiculos"):
            resultados = self.logica.buscar_vehiculos(criterio)
        else:
            resultados = []

        if not resultados:
            lbl_vacio = ctk.CTkLabel(
                self.tabla_container, 
                text="⚠️ No hay registros que coincidan con la búsqueda.", 
                font=self.font_body,
                text_color="#8E8E93"
            )
            lbl_vacio.pack(pady=40)
            return

        # D. Pintar las tarjetas de resultados
        for vehiculo in resultados:
            # 1. Tarjeta contenedora principal
            card_item = ctk.CTkFrame(
                self.tabla_container,
                fg_color="#262626",
                corner_radius=8,
                border_width=1,
                border_color="#3A3A3A"
            )
            card_item.pack(fill="x", padx=10, pady=6)
            card_item.configure(cursor="hand2") # Cambia el cursor a manito para indicar que es cliqueable


            info_basica_frame = ctk.CTkFrame(card_item, fg_color="transparent")
            info_basica_frame.pack(fill="x", padx=12, pady=8)

            tipo_txt = f"【 {vehiculo.get('tipo', 'VEHÍCULO')} 】 - {vehiculo.get('subcategoria', 'N/A')} - ESTADO: {vehiculo.get('estado', 'N/A')}"
            info_principal = f"{vehiculo.get('marca', 'S/M')} {vehiculo.get('modelo', 'S/M')} – Color: {vehiculo.get('color', 'S/C')}"
            datos_identificacion = f"Chapa/Matrícula: {vehiculo.get('matricula', 'S/D')}  |  N° de Chasis: {vehiculo.get('chasis', 'S/D')}"
            propietario = f"Titular: {vehiculo.get('inscripto_nombre', 'Desconocido')} (Documento N°: {vehiculo.get('ci_num', 'S/N')})"
            

            lbl_tipo = ctk.CTkLabel(info_basica_frame, text=tipo_txt, font=ctk.CTkFont(size=11, weight="bold"), text_color="#3A9FBF")
            lbl_tipo.pack(anchor="w")
            
            lbl_prin = ctk.CTkLabel(info_basica_frame, text=info_principal, font=ctk.CTkFont(size=14, weight="bold"), text_color="#FFFFFF")
            lbl_prin.pack(anchor="w", pady=(2, 4))
            
            lbl_ident = ctk.CTkLabel(info_basica_frame, text=datos_identificacion, font=ctk.CTkFont(size=12), text_color="#2ECC71")
            lbl_ident.pack(anchor="w")
            
            lbl_prop = ctk.CTkLabel(info_basica_frame, text=propietario, font=ctk.CTkFont(size=11), text_color="#AAAAAA")
            lbl_prop.pack(anchor="w", pady=(2, 0))

            # 3. Contenedor Oculto para los detalles técnicos extras
            detalles_extras_frame = ctk.CTkFrame(card_item, fg_color="#1E1E1E", corner_radius=6)
            
            # Añadimos los datos específicos que faltaban
            extras_txt = (
                f"• Número de Registro Interno: {vehiculo.get('numero', 'S/N')}\n"
                f"• Año de Incautación: {vehiculo.get('ano_incautacion') or vehiculo.get('año incautacion') or 'S/D'}\n"
                f"• Unidad a Cargo: {vehiculo.get('unidad_a_cargo') or vehiculo.get('unidad_a_cargo') or 'Ninguna'}\n"
                f"• Observaciones / Ley Aplicada: {vehiculo.get('observacion', 'Sin observaciones escritas.')}"
            )
            
            lbl_extras = ctk.CTkLabel(
                detalles_extras_frame, 
                text=extras_txt, 
                font=ctk.CTkFont(size=12), 
                text_color="#DDDDDD",
                justify="left", 
                anchor="w",
                wraplength=600 # Evita que el texto largo rompa el diseño
            )
            lbl_extras.pack(fill="x", padx=15, pady=10)

            # 4. Función (Expandir / Colapsar)
            def alternar_tarjeta(event, frame_oculto=detalles_extras_frame):
                if frame_oculto.winfo_viewable():
                    frame_oculto.pack_forget() # Si está abierto, lo encoge
                else:
                    frame_oculto.pack(fill="x", padx=12, pady=(0, 10)) # Si está cerrado, lo muestra abajo

            # 5. Vinculamos el clic
            card_item.bind("<Button-1>", alternar_tarjeta)
            info_basica_frame.bind("<Button-1>", alternar_tarjeta)
            lbl_tipo.bind("<Button-1>", alternar_tarjeta)
            lbl_prin.bind("<Button-1>", alternar_tarjeta)
            lbl_ident.bind("<Button-1>", alternar_tarjeta)
            lbl_prop.bind("<Button-1>", alternar_tarjeta)