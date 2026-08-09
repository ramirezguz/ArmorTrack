import json
import os
import customtkinter as ctk
from Presentation.visual_tk import mostrar_alerta


class FormularioVehiculo(ctk.CTkFrame):
    def __init__(self, parent, registro_logica=None):
        super().__init__(parent, fg_color="transparent")
        self.parent = parent
        self.logica = registro_logica

        # Estructura para guardar los datos JSON cargados en memoria
        self.datos_marcas_modelos = {}

        # Definición de fuentes
        self.font_title = ("SF Pro Display", 18, "bold")
        self.font_label = ("SF Pro Text", 12, "bold")
        self.font_body = ("SF Pro Text", 12)

        # Construir la interfaz de usuario
        self.crear_componentes()

        # Cargar datos iniciales del primer tipo seleccionado
        self.evento_cambio_tipo(self.combo_tipo.get())

    def cargar_datos_json(self, tipo):
        """Lee el archivo JSON desde la carpeta Database según el tipo seleccionado."""
        ruta_base = os.path.join(os.path.dirname(__file__), "..", "Database")

        if tipo == "MOTOCICLETA":
            archivo_path = os.path.join(ruta_base, "motocicletas.json")
        else:
            archivo_path = os.path.join(ruta_base, "vehiculos.json")

        try:
            if os.path.exists(archivo_path):
                with open(archivo_path, "r", encoding="utf-8") as file:
                    self.datos_marcas_modelos = json.load(file)
                    marcas = list(self.datos_marcas_modelos.keys())
                    marcas.append("OTRO...")
                    return marcas
        except Exception as e:
            print(f"Error al cargar archivo JSON ({archivo_path}): {e}")

        self.datos_marcas_modelos = {}
        return ["OTRO..."]

    def evento_cambio_tipo(self, tipo):
        """Se ejecuta cuando el usuario cambia entre VEHÍCULO y MOTOCICLETA."""
        if tipo == "VEHÍCULO":
            # CORREGIDO: Uso de .grid nativo sin parámetros inválidos. Ubicado debajo de Tipo de Vehículo.
            self.lbl_subcategoria.grid(row=4, column=0, sticky="w", padx=20, pady=(10, 5))
            self.combo_subcategoria.grid(row=5, column=0, sticky="ew", padx=20, pady=(0, 15))
        else:
            self.lbl_subcategoria.grid_forget()
            self.combo_subcategoria.grid_forget()
            self.txt_otra_subcategoria.grid_forget()

        # Carga de marcas
        if self.logica and hasattr(self.logica, "obtener_marcas_por_tipo"):
            marcas = self.logica.obtener_marcas_por_tipo(tipo)
            if "OTRO..." not in marcas:
                marcas.append("OTRO...")
        else:
            marcas = self.cargar_datos_json(tipo)

        if hasattr(self, "combo_marca") and marcas:
            self.combo_marca.configure(values=marcas)
            primera_marca = marcas[0]
            self.combo_marca.set(primera_marca)

            # Carga automáticamente los modelos de la primera marca
            self.evento_cambio_marca(primera_marca)

    def evento_cambio_marca(self, marca_seleccionada):
        """Maneja el comportamiento dinámico al cambiar de Marca."""
        if marca_seleccionada == "OTRO...":

            self.txt_otra_marca.grid(row=8, column=0, sticky="ew", padx=20, pady=(0, 15))
            self.txt_otra_marca.focus()

            self.combo_modelo.configure(values=["OTRO..."])
            self.combo_modelo.set("OTRO...")
            self.txt_otro_modelo.grid(row=11, column=0, sticky="ew", padx=20, pady=(0, 15))
        else:

            self.txt_otra_marca.grid_forget()

            modelos = list(self.datos_marcas_modelos.get(marca_seleccionada, []))
            modelos.append("OTRO...")

            if hasattr(self, "combo_modelo") and modelos:
                self.combo_modelo.configure(values=modelos)
                primera_opcion_modelo = modelos[0]
                self.combo_modelo.set(primera_opcion_modelo)
                
                self.evento_cambio_modelo(primera_opcion_modelo)

    def evento_cambio_subcategoria(self, subcategoria_seleccionada):
        """Maneja la visibilidad del campo de texto cuando se elige 'OTROS' en subcategoría."""
        if subcategoria_seleccionada == "OTROS" and self.combo_tipo.get() == "VEHÍCULO":

            self.txt_otra_subcategoria.grid(row=6, column=0, sticky="ew", padx=20, pady=(0, 15))
            self.txt_otra_subcategoria.focus()
        else:
            self.txt_otra_subcategoria.grid_forget()

    def evento_cambio_modelo(self, modelo_seleccionado):
        """Maneja la visibilidad del campo de texto de modelo."""
        if modelo_seleccionado == "OTRO...":
            self.txt_otro_modelo.grid(row=11, column=0, sticky="ew", padx=20, pady=(0, 15))
            self.txt_otro_modelo.focus()
        else:
            self.txt_otro_modelo.grid_forget()

    def evento_cambio_unidad(self, unidad_seleccionada):
        """Maneja la visibildiad del campo Unidad."""
        if unidad_seleccionada == "OTRO...":
            self.txt_otra_unidad.grid(row=15, column=0, sticky="ew", padx=20, pady=(0, 15))
            self.txt_otra_unidad.focus()
        else:
            self.txt_otra_unidad.grid_forget()

    def crear_componentes(self):
        # Título Superior
        self.lbl_titulo = ctk.CTkLabel(
            self,
            text="REGISTRO / INCAUTACIÓN DE VEHÍCULOS",
            font=self.font_title
        )
        self.lbl_titulo.pack(pady=(0, 15))

        # Tarjeta deslizable contenedora
        self.card = ctk.CTkScrollableFrame(
            self,
            fg_color="#262626",
            corner_radius=12,
            border_width=1,
            border_color="#333333"
        )
        self.card.pack(fill="both", expand=True, padx=10, pady=5)

        # Contenedor intermedio transparente dentro de la tarjeta
        self.form_container = ctk.CTkFrame(self.card, fg_color="transparent")
        self.form_container.pack(fill="x", expand=True, padx=10, pady=5)

        # Configuración equilibrada de las dos columnas principales
        self.form_container.grid_columnconfigure(0, weight=1)
        self.form_container.grid_columnconfigure(1, weight=1)

        # ==================== COLUMNA 0 (IZQUIERDA) ====================
        
        # ------------ 1. ESTADO ------------
        lbl_estado_title = ctk.CTkLabel(self.form_container, text="Estado:", font=self.font_label)
        lbl_estado_title.grid(row=0, column=0, sticky="w", padx=20, pady=(15, 5))
        
        self.combo_estado = ctk.CTkOptionMenu(
            self.form_container,
            values=["INCAUTADO", "DEPOSITADO"],
            font=self.font_body,
            dropdown_font=self.font_body,
            fg_color="#3A3A3C",
            button_color="#48484A",
            button_hover_color="#007AFF",
            dropdown_fg_color="#2D2D2D",
            dropdown_hover_color="#007AFF",
            corner_radius=8,
            height=36,
        )
        self.combo_estado.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 15))

        # ------------ 2. TIPO DE VEHÍCULO ------------
        lbl_tipo_title = ctk.CTkLabel(self.form_container, text="Tipo de Vehículo:", font=self.font_label)
        lbl_tipo_title.grid(row=2, column=0, sticky="w", padx=20, pady=(10, 5))

        self.combo_tipo = ctk.CTkOptionMenu(
            self.form_container,
            values=["VEHÍCULO", "MOTOCICLETA"],
            font=self.font_body,
            dropdown_font=self.font_body,
            fg_color="#3A3A3C",
            button_color="#48484A",
            button_hover_color="#007AFF",
            dropdown_fg_color="#2D2D2D",
            dropdown_hover_color="#007AFF",
            corner_radius=8,
            height=36,
            command=self.evento_cambio_tipo
        )
        self.combo_tipo.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 15))

        # ------------ 3. SUBCATEGORÍA ------------
        self.lbl_subcategoria = ctk.CTkLabel(self.form_container, text="Subcategoría / Carrocería:", font=self.font_label)
        self.combo_subcategoria = ctk.CTkOptionMenu(
            self.form_container,
            values=["AUTOMOVIL", "CAMIONETA", "CAMION", "OMNIBUS", "OTROS"],
            font=self.font_body,
            dropdown_font=self.font_body,
            fg_color="#3A3A3C",
            button_color="#48484A",
            button_hover_color="#007AFF",
            dropdown_fg_color="#2D2D2D",
            dropdown_hover_color="#007AFF",
            corner_radius=8,
            height=36,
            command=self.evento_cambio_subcategoria
        )
        
        # Campo dinámico para Nueva Subcategoría
        self.txt_otra_subcategoria = ctk.CTkEntry(
            self.form_container,
            placeholder_text="Escriba nueva SUBCATEGORIA...",
            font=self.font_body,
            fg_color="#1E1E1E",
            border_color="#007AFF",
            corner_radius=8,
            height=38
        )

        # ------------ 4. MARCA ------------
        lbl_marca_title = ctk.CTkLabel(self.form_container, text="Marca:", font=self.font_label)
        lbl_marca_title.grid(row=7, column=0, sticky="w", padx=20, pady=(10, 5))

        self.combo_marca = ctk.CTkOptionMenu(
            self.form_container,
            values=["Cargando..."],
            font=self.font_body,
            dropdown_font=self.font_body,
            fg_color="#3A3A3C",
            button_color="#48484A",
            button_hover_color="#007AFF",
            dropdown_fg_color="#2D2D2D",
            dropdown_hover_color="#007AFF",
            corner_radius=8,
            height=36,
            command=self.evento_cambio_marca
        )
        self.combo_marca.grid(row=8, column=0, sticky="ew", padx=20, pady=(0, 15))

        # Campo dinámico para Nueva Marca
        self.txt_otra_marca = ctk.CTkEntry(
            self.form_container,
            placeholder_text="Escriba la NUEVA MARCA...",
            font=self.font_body,
            fg_color="#1E1E1E",
            border_color="#007AFF",
            corner_radius=8,
            height=38
        )

        # ------------ 5. MODELO ------------
        lbl_modelo_title = ctk.CTkLabel(self.form_container, text="Modelo:", font=self.font_label)
        lbl_modelo_title.grid(row=9, column=0, sticky="w", padx=20, pady=(10, 5))

        self.combo_modelo = ctk.CTkOptionMenu(
            self.form_container,
            values=["Cargando..."],
            font=self.font_body,
            dropdown_font=self.font_body,
            fg_color="#3A3A3C",
            button_color="#48484A",
            button_hover_color="#007AFF",
            dropdown_fg_color="#2D2D2D",
            dropdown_hover_color="#007AFF",
            corner_radius=8,
            height=36,
            command=self.evento_cambio_modelo
        )
        self.combo_modelo.grid(row=10, column=0, sticky="ew", padx=20, pady=(0, 15))

        # Campo dinámico para Nuevo Modelo
        self.txt_otro_modelo = ctk.CTkEntry(
            self.form_container,
            placeholder_text="Escriba el NUEVO MODELO...",
            font=self.font_body,
            fg_color="#1E1E1E",
            border_color="#007AFF",
            corner_radius=8,
            height=38
        )


        # ------------ 5. UNIDAD A CARGO ------------
        lbl_unidad_title = ctk.CTkLabel(self.form_container, text="Unidad a Cargo:", font=self.font_label)
        lbl_unidad_title.grid(row=12, column=0, sticky="w", padx=20, pady=(10, 5))

        self.combo_unidad = ctk.CTkOptionMenu(
            self.form_container,
            values=["UNIDAD 1", "UNIDAD 2", "UNIDAD 3", "UNIDAD 4", "OTRO..."],
            font=self.font_body,
            dropdown_font=self.font_body,
            fg_color="#3A3A3C",
            button_color="#48484A",
            button_hover_color="#007AFF",
            dropdown_fg_color="#2D2D2D",
            dropdown_hover_color="#007AFF",
            corner_radius=8,
            height=36,
            command=self.evento_cambio_unidad
        )
        self.combo_unidad.grid(row=13, column=0, sticky="ew", padx=20, pady=(0, 15))

        # Campo dinámico para Nueva Unidad
        self.txt_otra_unidad = ctk.CTkEntry(
            self.form_container,
            placeholder_text="Escriba Nueva Unidad",
            font=self.font_body,
            fg_color="#1E1E1E",
            border_color="#007AFF",
            corner_radius=8,
            height=38
        )

        # ==================== COLUMNA 1 (DERECHA) ====================
        
        # ------------ 6. MATRÍCULA / CHAPA ------------
        lbl_chapa = ctk.CTkLabel(self.form_container, text="Matrícula / Chapa:", font=self.font_label)
        lbl_chapa.grid(row=0, column=1, sticky="w", padx=20, pady=(15, 5))

        self.txt_chapa = ctk.CTkEntry(
            self.form_container,
            placeholder_text="Ej: ABC123",
            font=self.font_body,
            fg_color="#1E1E1E",
            border_color="#3A3A3A",
            corner_radius=8,
            height=38
        )
        self.txt_chapa.grid(row=1, column=1, sticky="ew", padx=20, pady=(0, 15))

        # ------------ 7. N° DE CHASIS ------------
        lbl_chasis = ctk.CTkLabel(self.form_container, text="N° de Chasis:", font=self.font_label)
        lbl_chasis.grid(row=2, column=1, sticky="w", padx=20, pady=(10, 5))

        self.txt_chasis = ctk.CTkEntry(
            self.form_container,
            placeholder_text="Número de chasis...",
            font=self.font_body,
            fg_color="#1E1E1E",
            border_color="#3A3A3A",
            corner_radius=8,
            height=38
        )
        self.txt_chasis.grid(row=3, column=1, sticky="ew", padx=20, pady=(0, 15))

        # ------------ 8. COLOR ------------
        lbl_color = ctk.CTkLabel(self.form_container, text="Color:", font=self.font_label)
        lbl_color.grid(row=4, column=1, sticky="w", padx=20, pady=(10, 5))

        self.txt_color = ctk.CTkEntry(
            self.form_container,
            placeholder_text="Ej: Blanco, Negro, Rojo...",
            font=self.font_body,
            fg_color="#1E1E1E",
            border_color="#3A3A3A",
            corner_radius=8,
            height=38
        )
        self.txt_color.grid(row=5, column=1, sticky="ew", padx=20, pady=(0, 15))

        # ------------ 9. INSCRIPTO A NOMBRE DE ------------
        lbl_inscripto = ctk.CTkLabel(self.form_container, text="Inscripto a Nombre de:", font=self.font_label)
        lbl_inscripto.grid(row=7, column=1, sticky="w", padx=20, pady=(10, 5))

        self.txt_inscripto = ctk.CTkEntry(
            self.form_container,
            placeholder_text="Ej: Maria Benitez",
            font=self.font_body,
            fg_color="#1E1E1E",
            border_color="#3A3A3A",
            corner_radius=8,
            height=38
        )
        self.txt_inscripto.grid(row=8, column=1, sticky="ew", padx=20, pady=(0, 15))

        # ------------ 10. DOCUMENTO N° ------------
        lbl_documento_num = ctk.CTkLabel(self.form_container, text="Documento N°:", font=self.font_label)
        lbl_documento_num.grid(row=9, column=1, sticky="w", padx=20, pady=(10, 5))

        self.txt_documento_num = ctk.CTkEntry(
            self.form_container,
            placeholder_text="Documento N°",
            font=self.font_body,
            fg_color="#1E1E1E",
            border_color="#3A3A3A",
            corner_radius=8,
            height=38
        )
        self.txt_documento_num.grid(row=10, column=1, sticky="ew", padx=20, pady=(0, 15))


        # ==================== BOTÓN DE GUARDAR (CENTRADOS) ====================
        self.btn_guardar = ctk.CTkButton(
            self.form_container,
            text="Guardar Registro",
            font=("SF Pro Text", 13, "bold"),
            fg_color="#34C759",
            hover_color="#28A745",
            corner_radius=8,
            height=42,
            command=self.guardar_registro
        )
        # Ocupa ambas columnas para mantenerse abajo y perfectamente centrado
        self.btn_guardar.grid(row=18, column=0, columnspan=2, pady=30, padx=20, sticky="ew")

    def obtener_subcategoria_final(self):
        """Retorna la subcategoría seleccionada, la escrita manualmente, o 'N/A'."""
        if self.combo_tipo.get() == "VEHÍCULO":
            subcat = self.combo_subcategoria.get()
            if subcat == "OTROS":
                otra = self.txt_otra_subcategoria.get().strip().upper()
                return otra if otra else "OTRO (NO ESPECIFICADO)"
            return subcat
        return "MOTOCICLETA"

    def obtener_marca_final(self):
        """Retorna la marca seleccionada o la escrita manualmente."""
        marca = self.combo_marca.get()
        if marca == "OTRO...":
            otra = self.txt_otra_marca.get().strip().upper()
            return otra if otra else "DESCONOCIDO"
        return marca

    def obtener_unidad_final(self):
        """Retorna la unidad seleccionada o la escrita manualmente."""
        unidad = self.combo_unidad.get()
        if unidad == "OTRO...":
            otra = self.txt_otra_unidad.get().strip().upper()
            return otra if otra else "DESCONOCIDO"
        return unidad

    def obtener_modelo_final(self):
        """Retorna el modelo seleccionado o el escrito manualmente."""
        modelo = self.combo_modelo.get()
        if modelo == "OTRO...":
            otro = self.txt_otro_modelo.get().strip().upper()
            return otro if otro else "DESCONOCIDO"
        return modelo

    def guardar_registro(self):
        """Recopila todos los datos del formulario."""
        datos = {
            "estado": self.combo_estado.get(),
            "tipo": self.combo_tipo.get(),
            "subcategoria": self.obtener_subcategoria_final(),
            "marca": self.obtener_marca_final(),
            "modelo": self.obtener_modelo_final(),
            "color": self.txt_color.get().strip(),
            "Matricula": self.txt_chapa.get().strip().upper(),
            "chasis": self.txt_chasis.get().strip().upper(),
            "Inscripto a Nombre de": self.txt_inscripto.get().strip(),
            "C_I_N°": self.txt_documento_num.get().strip(),
            "unidad_a_cargo": self.obtener_unidad_final()
        }
        
        if self.logica and hasattr(self.logica, "registrar_vehiculo"):
            exito, mensaje = self.logica.registrar_vehiculo(datos)
            if exito:
                mostrar_alerta(self, "Éxito", "El vehículo fue incautado y registrado con éxito.", "success")
                
                # Limpiar campos
                self.txt_chapa.delete(0, 'end')
                self.txt_chasis.delete(0, 'end')
                self.txt_color.delete(0, 'end')
                self.txt_inscripto.delete(0, 'end')
                self.txt_documento_num.delete(0, 'end')
            else:
                mostrar_alerta(self, "Error", f"Ocurrió un problema: {mensaje}", "error")
        else:
            mostrar_alerta(self, "Modo Demo", "Registro simulado correctamente.", "info")