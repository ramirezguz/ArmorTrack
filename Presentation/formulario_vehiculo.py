import json
import os
import customtkinter as ctk


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
        # Manejo visual de la Subcategoría
        if tipo == "VEHÍCULO":
            self.lbl_subcategoria.pack(after=self.combo_tipo, anchor="w", padx=20, pady=(5, 5))
            self.combo_subcategoria.pack(after=self.lbl_subcategoria, fill="x", padx=20, pady=(0, 15))
        else:
            # Ocultar subcategoría si es MOTOCICLETA
            self.lbl_subcategoria.pack_forget()
            self.combo_subcategoria.pack_forget()
            self.txt_otra_subcategoria.pack_forget()

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
            # 1. MOSTRAR campo de Nueva Marca justo debajo del combo de Marca
            self.txt_otra_marca.pack(after=self.combo_marca, fill="x", padx=20, pady=(0, 15))
            self.txt_otra_marca.focus()

            # 2. Configurar Modelo en OTRO... y MOSTRAR campo de Nuevo Modelo debajo del combo de Modelo
            self.combo_modelo.configure(values=["OTRO..."])
            self.combo_modelo.set("OTRO...")
            self.txt_otro_modelo.pack(after=self.combo_modelo, fill="x", padx=20, pady=(0, 15))

        else:
            # 1. OCULTAR campo de Nueva Marca
            self.txt_otra_marca.pack_forget()

            # 2. Obtener la lista de modelos de esa marca
            modelos = list(self.datos_marcas_modelos.get(marca_seleccionada, []))
            modelos.append("OTRO...")

            if hasattr(self, "combo_modelo") and modelos:
                self.combo_modelo.configure(values=modelos)
                primera_opcion_modelo = modelos[0]
                self.combo_modelo.set(primera_opcion_modelo)
                
                # Evaluar si el primer modelo requiere mostrar/ocultar el campo de texto
                self.evento_cambio_modelo(primera_opcion_modelo)

    def evento_cambio_subcategoria(self, subcategoria_seleccionada):
        """Maneja la visibilidad del campo de texto cuando se elige 'OTROS' en subcategoría."""
        if subcategoria_seleccionada == "OTROS":
            # Lo posicionamos justo debajo del combo de subcategoría
            self.txt_otra_subcategoria.pack(after=self.combo_subcategoria, fill="x", padx=20, pady=(0, 15))
            self.txt_otra_subcategoria.focus()
        else:
            self.txt_otra_subcategoria.pack_forget()

    def evento_cambio_modelo(self, modelo_seleccionado):
        """Maneja la visibilidad del campo de texto de modelo justo debajo del combo correspondiente."""
        if modelo_seleccionado == "OTRO...":
            self.txt_otro_modelo.pack(after=self.combo_modelo, fill="x", padx=20, pady=(0, 15))
            self.txt_otro_modelo.focus()
        else:
            self.txt_otro_modelo.pack_forget()

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

        # ---------------- 1. TIPO DE VEHÍCULO ----------------
        lbl_tipo_title = ctk.CTkLabel(self.card, text="Tipo de Vehículo:", font=self.font_label)
        lbl_tipo_title.pack(anchor="w", padx=20, pady=(15, 5))

        self.combo_tipo = ctk.CTkOptionMenu(
            self.card,
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
        self.combo_tipo.pack(fill="x", padx=20, pady=(0, 15))

        # ---------------- 1.5 SUBCATEGORÍA (AUTOMÓVIL, CAMIONETA, ETC.) ----------------
        self.lbl_subcategoria = ctk.CTkLabel(self.card, text="Subcategoría / Carrocería:", font=self.font_label)
        self.combo_subcategoria = ctk.CTkOptionMenu(
            self.card,
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
                # Campo dinámico para Nuevo Tipo
        self.txt_otra_subcategoria = ctk.CTkEntry(
            self.card,
            placeholder_text="Escriba nueva SUBCATEGORIA...",
            font=self.font_body,
            fg_color="#1E1E1E",
            border_color="#007AFF",
            corner_radius=8,
            height=38
        )


        # ---------------- 2. MARCA ----------------
        lbl_marca_title = ctk.CTkLabel(self.card, text="Marca:", font=self.font_label)
        lbl_marca_title.pack(anchor="w", padx=20, pady=(5, 5))

        self.combo_marca = ctk.CTkOptionMenu(
            self.card,
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
        self.combo_marca.pack(fill="x", padx=20, pady=(0, 15))

        # Campo dinámico para Nueva Marca
        self.txt_otra_marca = ctk.CTkEntry(
            self.card,
            placeholder_text="Escriba la NUEVA MARCA...",
            font=self.font_body,
            fg_color="#1E1E1E",
            border_color="#007AFF",
            corner_radius=8,
            height=38
        )

        # ---------------- 3. MODELO ----------------
        lbl_modelo_title = ctk.CTkLabel(self.card, text="Modelo:", font=self.font_label)
        lbl_modelo_title.pack(anchor="w", padx=20, pady=(5, 5))

        self.combo_modelo = ctk.CTkOptionMenu(
            self.card,
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
        self.combo_modelo.pack(fill="x", padx=20, pady=(0, 15))

        # Campo dinámico para Nuevo Modelo
        self.txt_otro_modelo = ctk.CTkEntry(
            self.card,
            placeholder_text="Escriba el NUEVO MODELO...",
            font=self.font_body,
            fg_color="#1E1E1E",
            border_color="#007AFF",
            corner_radius=8,
            height=38
        )

        # ---------------- 4. MATRÍCULA / CHASSIS / COLOR ----------------
        lbl_chapa = ctk.CTkLabel(self.card, text="Matrícula / Chapa:", font=self.font_label)
        lbl_chapa.pack(anchor="w", padx=20, pady=(5, 5))

        self.txt_chapa = ctk.CTkEntry(
            self.card,
            placeholder_text="Ej: ABC 123",
            font=self.font_body,
            fg_color="#1E1E1E",
            border_color="#3A3A3A",
            corner_radius=8,
            height=38
        )
        self.txt_chapa.pack(fill="x", padx=20, pady=(0, 15))

        lbl_chasis = ctk.CTkLabel(self.card, text="N° de Chasis / Bastidor:", font=self.font_label)
        lbl_chasis.pack(anchor="w", padx=20, pady=(5, 5))

        self.txt_chasis = ctk.CTkEntry(
            self.card,
            placeholder_text="Número de chasis...",
            font=self.font_body,
            fg_color="#1E1E1E",
            border_color="#3A3A3A",
            corner_radius=8,
            height=38
        )
        self.txt_chasis.pack(fill="x", padx=20, pady=(0, 15))

        lbl_color = ctk.CTkLabel(self.card, text="Color:", font=self.font_label)
        lbl_color.pack(anchor="w", padx=20, pady=(5, 5))

        self.txt_color = ctk.CTkEntry(
            self.card,
            placeholder_text="Ej: Blanco, Negro, Rojo...",
            font=self.font_body,
            fg_color="#1E1E1E",
            border_color="#3A3A3A",
            corner_radius=8,
            height=38
        )
        self.txt_color.pack(fill="x", padx=20, pady=(0, 20))

                # ----------------5. INSCRIPTO A NOMBRE DE / DOCUMENTO N°----------------
        lbl_inscripto = ctk.CTkLabel(self.card, text="Inscripto a Nombre de:", font=self.font_label)
        lbl_inscripto.pack(anchor="w", padx=20, pady=(5, 5))

        self.txt_inscripto = ctk.CTkEntry(
            self.card,
            placeholder_text="Ej: Maria Benitez",
            font=self.font_body,
            fg_color="#1E1E1E",
            border_color="#3A3A3A",
            corner_radius=8,
            height=38
        )
        self.txt_inscripto.pack(fill="x", padx=20, pady=(0, 15))

        lbl_documento_num = ctk.CTkLabel(self.card, text="Documento N°:", font=self.font_label)
        lbl_documento_num.pack(anchor="w", padx=20, pady=(5, 5))

        self.txt_documento_num = ctk.CTkEntry(
            self.card,
            placeholder_text="Documento N°",
            font=self.font_body,
            fg_color="#1E1E1E",
            border_color="#3A3A3A",
            corner_radius=8,
            height=38
        )
        self.txt_documento_num.pack(fill="x", padx=20, pady=(0, 15))

        

        # ---------------- BOTÓN DE GUARDAR ----------------
        self.btn_guardar = ctk.CTkButton(
            self.card,
            text="Guardar Registro",
            font=("SF Pro Text", 13, "bold"),
            fg_color="#34C759",
            hover_color="#28A745",
            corner_radius=8,
            height=42,
            command=self.guardar_registro
        )
        self.btn_guardar.pack(fill="x", padx=20, pady=(10, 25))

    def obtener_subcategoria_final(self):
        """Retorna la subcategoría seleccionada, la escrita manualmente, o 'N/A'."""
        if self.combo_tipo.get() == "VEHÍCULO":
            subcat = self.combo_subcategoria.get()
            if subcat == "OTROS":
                otra = self.txt_otra_subcategoria.get().strip().upper()
                return otra if otra else "OTRO (NO ESPECIFICADO)"
            return subcat
        return "N/A"

    def obtener_marca_final(self):
        """Retorna la marca seleccionada o la escrita manualmente."""
        marca = self.combo_marca.get()
        if marca == "OTRO...":
            otra = self.txt_otra_marca.get().strip().upper()
            return otra if otra else "DESCONOCIDO"
        return marca

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
            "tipo": self.combo_tipo.get(),
            "subcategoria": self.obtener_subcategoria_final(),
            "marca": self.obtener_marca_final(),
            "modelo": self.obtener_modelo_final(),
            "chapa": self.txt_chapa.get().strip().upper(),
            "chasis": self.txt_chasis.get().strip().upper(),
            "color": self.txt_color.get().strip()
        }

        if self.logica and hasattr(self.logica, "registrar_vehiculo"):
            self.logica.registrar_vehiculo(datos)
            print("Registro procesado por la capa lógica:", datos)
        else:
            print("Datos registrados con éxito (Modo Demo):", datos)