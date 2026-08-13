import json
import os
import customtkinter as ctk
from Presentation.visual_tk import mostrar_alerta

class FormularioVehiculo(ctk.CTkFrame):
    def __init__(self, parent, registro_logica=None):
        super().__init__(parent, fg_color="transparent")
        self.parent = parent
        self.logica = registro_logica

        self.paso_actual = 1
        self.datos_marcas_modelos = {}

        self.font_title = ("SF Pro Display", 18, "bold")
        self.font_label = ("SF Pro Text", 12, "bold")
        self.font_body = ("SF Pro Text", 12)

        self.crear_estructura_base()
        self.crear_paso_1_vehiculo()
        self.crear_paso_2_conductor()
        self.crear_paso_3_judicial()
        self.actualizar_flujo()

    def crear_estructura_base(self):
        """Inicializa los componentes principales de la interfaz y navegacion."""
        self.lbl_titulo = ctk.CTkLabel(self, text="REGISTRO INTEGRAL DE OPERATIVOS", font=self.font_title)
        self.lbl_titulo.pack(pady=(0, 10))

        self.frame_pasos_indicador = ctk.CTkFrame(self, fg_color="#1E1E1E", height=40, corner_radius=8)
        self.frame_pasos_indicador.pack(fill="x", padx=10, pady=(0, 15))
        
        self.lbl_indicador = ctk.CTkLabel(
            self.frame_pasos_indicador, 
            text="🔵 VEHÍCULO   ➔   ⚪ CONDUCTOR   ➔   ⚪ JUDICIAL", 
            font=("SF Pro Text", 13, "bold"),
            text_color="#AEAEB2"
        )
        self.lbl_indicador.pack(expand=True, pady=8)

        self.card = ctk.CTkScrollableFrame(self, fg_color="#262626", corner_radius=12, border_width=1, border_color="#333333")
        self.card.pack(fill="both", expand=True, padx=10, pady=5)

        self.frame_navegacion = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_navegacion.pack(fill="x", padx=10, pady=15)

        self.btn_atras = ctk.CTkButton(
            self.frame_navegacion, text="◀ Atrás", font=self.font_label,
            fg_color="#48484A", hover_color="#3A3A3C", height=40, command=self.retroceder_paso
        )
        self.btn_atras.pack(side="left", padx=10)

        self.btn_siguiente = ctk.CTkButton(
            self.frame_navegacion, text="Siguiente ▶", font=self.font_label,
            fg_color="#007AFF", hover_color="#0056B3", height=40, command=self.avanzar_paso
        )
        self.btn_siguiente.pack(side="right", padx=10)

    def crear_paso_1_vehiculo(self):
        """Inicializa los campos de datos del vehiculo."""
        self.frame_paso1 = ctk.CTkFrame(self.card, fg_color="transparent")
        self.frame_paso1.grid_columnconfigure(0, weight=1)
        self.frame_paso1.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.frame_paso1, text="Estado:", font=self.font_label).grid(row=0, column=0, sticky="w", padx=20, pady=(10, 5))
        self.combo_estado = ctk.CTkOptionMenu(self.frame_paso1, values=["INCAUTADO", "DEPOSITADO"], font=self.font_body, height=36, fg_color="#3A3A3C")
        self.combo_estado.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))

        ctk.CTkLabel(self.frame_paso1, text="Tipo de Vehículo:", font=self.font_label).grid(row=2, column=0, sticky="w", padx=20, pady=(10, 5))
        self.combo_tipo = ctk.CTkOptionMenu(self.frame_paso1, values=["VEHÍCULO", "MOTOCICLETA"], font=self.font_body, height=36, fg_color="#3A3A3C", command=self.evento_cambio_tipo)
        self.combo_tipo.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 10))

        self.lbl_subcategoria = ctk.CTkLabel(self.frame_paso1, text="Subcategoría / Carrocería:", font=self.font_label)
        self.combo_subcategoria = ctk.CTkOptionMenu(self.frame_paso1, values=["AUTOMOVIL", "CAMIONETA", "CAMION", "OMNIBUS", "OTROS"], font=self.font_body, height=36, fg_color="#3A3A3C", command=self.evento_cambio_subcategoria)
        self.txt_otra_subcategoria = ctk.CTkEntry(self.frame_paso1, placeholder_text="Escriba nueva SUBCATEGORIA...", font=self.font_body, height=38, border_color="#007AFF")

        ctk.CTkLabel(self.frame_paso1, text="Marca:", font=self.font_label).grid(row=7, column=0, sticky="w", padx=20, pady=(10, 5))
        self.combo_marca = ctk.CTkOptionMenu(self.frame_paso1, values=["Cargando..."], font=self.font_body, height=36, fg_color="#3A3A3C", command=self.evento_cambio_marca)
        self.combo_marca.grid(row=8, column=0, sticky="ew", padx=20, pady=(0, 10))
        self.txt_otra_marca = ctk.CTkEntry(self.frame_paso1, placeholder_text="Nueva Marca...", font=self.font_body, height=38, border_color="#007AFF")

        ctk.CTkLabel(self.frame_paso1, text="Modelo:", font=self.font_label).grid(row=9, column=0, sticky="w", padx=20, pady=(10, 5))
        self.combo_modelo = ctk.CTkOptionMenu(self.frame_paso1, values=["Cargando..."], font=self.font_body, height=36, fg_color="#3A3A3C", command=self.evento_cambio_modelo)
        self.combo_modelo.grid(row=10, column=0, sticky="ew", padx=20, pady=(0, 10))
        self.txt_otro_modelo = ctk.CTkEntry(self.frame_paso1, placeholder_text="Nuevo Modelo...", font=self.font_body, height=38, border_color="#007AFF")

        ctk.CTkLabel(self.frame_paso1, text="Matrícula / Chapa:", font=self.font_label).grid(row=0, column=1, sticky="w", padx=20, pady=(10, 5))
        self.txt_chapa = ctk.CTkEntry(self.frame_paso1, placeholder_text="Ej: ABC123", font=self.font_body, height=38, fg_color="#1E1E1E")
        self.txt_chapa.grid(row=1, column=1, sticky="ew", padx=20, pady=(0, 10))

        ctk.CTkLabel(self.frame_paso1, text="N° de Chasis:", font=self.font_label).grid(row=2, column=1, sticky="w", padx=20, pady=(10, 5))
        self.txt_chasis = ctk.CTkEntry(self.frame_paso1, placeholder_text="Número de chasis...", font=self.font_body, height=38, fg_color="#1E1E1E")
        self.txt_chasis.grid(row=3, column=1, sticky="ew", padx=20, pady=(0, 10))

        ctk.CTkLabel(self.frame_paso1, text="Color:", font=self.font_label).grid(row=4, column=1, sticky="w", padx=20, pady=(10, 5))
        self.txt_color = ctk.CTkEntry(self.frame_paso1, placeholder_text="Ej: Blanco, Negro...", font=self.font_body, height=38, fg_color="#1E1E1E")
        self.txt_color.grid(row=5, column=1, sticky="ew", padx=20, pady=(0, 10))

        ctk.CTkLabel(self.frame_paso1, text="Año:", font=self.font_label).grid(row=7, column=1, sticky="w", padx=20, pady=(10, 5))
        self.txt_ano_vehiculo = ctk.CTkEntry(self.frame_paso1, placeholder_text="Ej: 2026", font=self.font_body, height=38, fg_color="#1E1E1E")
        self.txt_ano_vehiculo.grid(row=8, column=1, sticky="ew", padx=20, pady=(0, 10))

        ctk.CTkLabel(self.frame_paso1, text="Inscripto a Nombre de:", font=self.font_label).grid(row=9, column=1, sticky="w", padx=20, pady=(10, 5))
        self.txt_inscripto = ctk.CTkEntry(self.frame_paso1, placeholder_text="Nombre del dueño titular", font=self.font_body, height=38, fg_color="#1E1E1E")
        self.txt_inscripto.grid(row=10, column=1, sticky="ew", padx=20, pady=(0, 10))

        ctk.CTkLabel(self.frame_paso1, text="C.I. N° del Titular:", font=self.font_label).grid(row=11, column=1, sticky="w", padx=20, pady=(10, 5))
        self.txt_documento_num = ctk.CTkEntry(self.frame_paso1, placeholder_text="C.I. N°", font=self.font_body, height=38, fg_color="#1E1E1E")
        self.txt_documento_num.grid(row=12, column=1, sticky="ew", padx=20, pady=(0, 10))

        self.evento_cambio_tipo(self.combo_tipo.get())

    def crear_paso_2_conductor(self):
        """Inicializa los campos de datos del conductor."""
        self.frame_paso2 = ctk.CTkFrame(self.card, fg_color="transparent")
        self.frame_paso2.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.frame_paso2, text="Nombre Completo del Conductor:", font=self.font_label).grid(row=0, column=0, sticky="w", padx=20, pady=(15, 5))
        self.txt_nombre_conductor = ctk.CTkEntry(self.frame_paso2, placeholder_text="Ej: Juan Ramón Benítez Ortiz", font=self.font_body, height=38, fg_color="#1E1E1E")
        self.txt_nombre_conductor.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 15))

        ctk.CTkLabel(self.frame_paso2, text="N° de Cédula de Identidad del Conductor:", font=self.font_label).grid(row=2, column=0, sticky="w", padx=20, pady=(10, 5))
        self.txt_ci_conductor = ctk.CTkEntry(self.frame_paso2, placeholder_text="Ej: 1234567 (Sin puntos)", font=self.font_body, height=38, fg_color="#1E1E1E")
        self.txt_ci_conductor.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 15))

    def crear_paso_3_judicial(self):
        """Inicializa los campos de datos judiciales."""
        self.frame_paso3 = ctk.CTkFrame(self.card, fg_color="transparent")
        self.frame_paso3.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.frame_paso3, text="Unidad Fiscal / Fiscalía interviniente:", font=self.font_label).grid(row=0, column=0, sticky="w", padx=20, pady=(15, 5))
        self.combo_unidad = ctk.CTkOptionMenu(self.frame_paso3, values=["UNIDAD 1", "UNIDAD 2", "UNIDAD 3", "UNIDAD 4", "OTRO..."], font=self.font_body, height=36, fg_color="#3A3A3C", command=self.evento_cambio_unidad)
        self.combo_unidad.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        self.txt_otra_unidad = ctk.CTkEntry(self.frame_paso3, placeholder_text="Escriba la nueva Unidad Fiscal...", font=self.font_body, height=38, border_color="#007AFF")

        ctk.CTkLabel(self.frame_paso3, text="Fecha de Incautación / Operativo:", font=self.font_label).grid(row=4, column=0, sticky="w", padx=20, pady=(10, 5))
        self.txt_fecha_incautacion = ctk.CTkEntry(self.frame_paso3, placeholder_text="Ej: DD/MM/AAAA", font=self.font_body, height=38, fg_color="#1E1E1E")
        self.txt_fecha_incautacion.grid(row=5, column=0, sticky="ew", padx=20, pady=(0, 15))

        ctk.CTkLabel(self.frame_paso3, text="Agente Fiscal a Cargo:", font=self.font_label).grid(row=6, column=0, sticky="w", padx=20, pady=(10, 5))
        self.txt_fiscal_a_cargo = ctk.CTkEntry(self.frame_paso3, placeholder_text="Abog. Nombre y Apellido", font=self.font_body, height=38, fg_color="#1E1E1E")
        self.txt_fiscal_a_cargo.grid(row=7, column=0, sticky="ew", padx=20, pady=(0, 15))

        ctk.CTkLabel(self.frame_paso3, text="Causa del Hecho / Observaciones:", font=self.font_label).grid(row=8, column=0, sticky="w", padx=20, pady=(10, 5))
        self.txt_causa_incautacion = ctk.CTkEntry(self.frame_paso3, placeholder_text="Ej: Exposición al Peligro en el Tránsito Terrestre, Alcoholemia...", font=self.font_body, height=38, fg_color="#1E1E1E")
        self.txt_causa_incautacion.grid(row=9, column=0, sticky="ew", padx=20, pady=(0, 15))

    def actualizar_flujo(self):
        """Alterna la visibilidad de los contenedores segun el paso actual."""
        self.frame_paso1.pack_forget()
        self.frame_paso2.pack_forget()
        self.frame_paso3.pack_forget()

        if self.paso_actual == 1:
            self.frame_paso1.pack(fill="x", expand=True)
            self.lbl_indicador.configure(text="🔵 VEHÍCULO   ➔   ⚪ CONDUCTOR   ➔   ⚪ DATOS JUDICIAL")
            self.btn_atras.configure(state="disabled")
            self.btn_siguiente.configure(text="Siguiente ▶", fg_color="#007AFF", hover_color="#0056B3")
        elif self.paso_actual == 2:
            self.frame_paso2.pack(fill="x", expand=True)
            self.lbl_indicador.configure(text="🟢 VEHÍCULO   ➔   🔵 CONDUCTOR   ➔   ⚪ DATOS JUDICIAL")
            self.btn_atras.configure(state="normal")
            self.btn_siguiente.configure(text="Siguiente ▶", fg_color="#007AFF", hover_color="#0056B3")
        elif self.paso_actual == 3:
            self.frame_paso3.pack(fill="x", expand=True)
            self.lbl_indicador.configure(text="🟢 VEHÍCULO   ➔   🟢 CONDUCTOR   ➔   🔵 DATOS JUDICIAL")
            self.btn_atras.configure(state="normal")
            self.btn_siguiente.configure(text="💾 Finalizar Guardado", fg_color="#34C759", hover_color="#28A745")

    def avanzar_paso(self):
        """Incrementa el contador de pasos de navegacion."""
        if self.paso_actual < 3:
            self.paso_actual += 1
            self.actualizar_flujo()
        else:
            self.guardar_registro_completo()

    def retroceder_paso(self):
        """Decrementa el contador de pasos de navegacion."""
        if self.paso_actual > 1:
            self.paso_actual -= 1
            self.actualizar_flujo()

    def cargar_datos_json(self, tipo):
        """Carga marcas y modelos desde origen JSON."""
        ruta_base = os.path.join(os.path.dirname(__file__), "..", "Database")
        archivo_path = os.path.join(ruta_base, "motocicletas.json" if tipo == "MOTOCICLETA" else "vehiculos.json")

        try:
            if os.path.exists(archivo_path):
                with open(archivo_path, "r", encoding="utf-8") as file:
                    self.datos_marcas_modelos = json.load(file)
                    marcas = list(self.datos_marcas_modelos.keys())
                    if "OTRO..." not in marcas:
                        marcas.append("OTRO...")
                    return marcas
        except Exception as e:
            print(f"Error archivo JSON ({archivo_path}): {e}")

        self.datos_marcas_modelos = {}
        return ["OTRO..."]

    def evento_cambio_tipo(self, tipo):
        """Maneja el cambio de seleccion en el menu de tipo de vehiculo."""
        if tipo == "VEHÍCULO":
            self.lbl_subcategoria.grid(row=4, column=0, sticky="w", padx=20, pady=(10, 5))
            self.combo_subcategoria.grid(row=5, column=0, sticky="ew", padx=20, pady=(0, 10))
        else:
            self.lbl_subcategoria.grid_forget()
            self.combo_subcategoria.grid_forget()
            self.txt_otra_subcategoria.grid_forget()

        marcas = self.cargar_datos_json(tipo)
        self.combo_marca.configure(values=marcas)
        self.combo_marca.set(marcas[0])
        self.evento_cambio_marca(marcas[0])

    def evento_cambio_marca(self, marca_seleccionada):
        """Maneja el cambio de seleccion en el menu de marcas."""
        if marca_seleccionada == "OTRO...":
            self.txt_otra_marca.grid(row=8, column=0, sticky="ew", padx=20, pady=(0, 10))
            self.combo_modelo.configure(values=["OTRO..."])
            self.combo_modelo.set("OTRO...")
            self.txt_otro_modelo.grid(row=11, column=0, sticky="ew", padx=20, pady=(0, 10))
        else:
            self.txt_otra_marca.grid_forget()
            modelos = list(self.datos_marcas_modelos.get(marca_seleccionada, []))
            modelos.append("OTRO...")
            self.combo_modelo.configure(values=modelos)
            self.combo_modelo.set(modelos[0])
            self.evento_cambio_modelo(modelos[0])

    def evento_cambio_subcategoria(self, subcat):
        """Maneja la visibilidad de entrada de texto manual para subcategoria."""
        if subcat == "OTROS" and self.combo_tipo.get() == "VEHÍCULO":
            self.txt_otra_subcategoria.grid(row=6, column=0, sticky="ew", padx=20, pady=(0, 10))
        else:
            self.txt_otra_subcategoria.grid_forget()

    def evento_cambio_modelo(self, mod):
        """Maneja la visibilidad de entrada de texto manual para modelo."""
        if mod == "OTRO...":
            self.txt_otro_modelo.grid(row=11, column=0, sticky="ew", padx=20, pady=(0, 10))
        else:
            self.txt_otro_modelo.grid_forget()

    def evento_cambio_unidad(self, uni):
        """Maneja la visibilidad de entrada de texto manual para unidad judicial."""
        if uni == "OTRO...":
            self.txt_otra_unidad.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 10))
        else:
            self.txt_otra_unidad.grid_forget()

    def obtener_subcategoria_final(self):
        """Procesa el valor de retorno para subcategoria."""
        if self.combo_tipo.get() == "VEHÍCULO":
            return self.txt_otra_subcategoria.get().strip().upper() if self.combo_subcategoria.get() == "OTROS" else self.combo_subcategoria.get()
        return "MOTOCICLETA"

    def obtener_marca_final(self):
        """Procesa el valor de retorno para marca."""
        return self.txt_otra_marca.get().strip().upper() if self.combo_marca.get() == "OTRO..." else self.combo_marca.get()

    def obtener_modelo_final(self):
        """Procesa el valor de retorno para modelo."""
        return self.txt_otro_modelo.get().strip().upper() if self.combo_modelo.get() == "OTRO..." else self.combo_modelo.get()

    def obtener_unidad_final(self):
        """Procesa el valor de retorno para la unidad fiscal."""
        return self.txt_otra_unidad.get().strip().upper() if self.combo_unidad.get() == "OTRO..." else self.combo_unidad.get()

    def guardar_registro_completo(self):
        """Recopila la informacion de los campos y ejecuta la persistencia."""
        datos = {
            "estado": self.combo_estado.get(),
            "tipo": self.combo_tipo.get(),
            "subcategoria": self.obtener_subcategoria_final(),
            "marca": self.obtener_marca_final(),
            "modelo": self.obtener_modelo_final(),
            "color": self.txt_color.get().strip(),
            "Matricula": self.txt_chapa.get().strip().upper(),
            "chasis": self.txt_chasis.get().strip().upper(),
            "ano_vehiculo": self.txt_ano_vehiculo.get().strip(),
            "Inscripto a Nombre de": self.txt_inscripto.get().strip(),
            "C_I_N°": self.txt_documento_num.get().strip(),
            "nombre_conductor": self.txt_nombre_conductor.get().strip(),
            "ci_conductor": self.txt_ci_conductor.get().strip(),
            "unidad_a_cargo": self.obtener_unidad_final(),
            "fecha_incautacion": self.txt_fecha_incautacion.get().strip(),
            "fiscal_a_cargo": self.txt_fiscal_a_cargo.get().strip(),
            "causa_incautacion": self.txt_causa_incautacion.get().strip()
        }
        
        if self.logica and hasattr(self.logica, "registrar_vehiculo"):
            exito, mensaje = self.logica.registrar_vehiculo(datos)
            if exito:
                mostrar_alerta(self, "Éxito Total", "El registro se guardó correctamente.", "success")
                self.limpiar_todo_el_asistente()
            else:
                mostrar_alerta(self, "Error", f"Fallo al insertar datos: {mensaje}", "error")
        else:
            mostrar_alerta(self, "Modo Demo", "Simulación de flujo exitosa.", "info")

    def limpiar_todo_el_asistente(self):
        """Restablece los valores por defecto de los campos de texto."""
        self.txt_chapa.delete(0, 'end')
        self.txt_chasis.delete(0, 'end')
        self.txt_color.delete(0, 'end')
        self.txt_ano_vehiculo.delete(0, 'end')
        self.txt_inscripto.delete(0, 'end')
        self.txt_documento_num.delete(0, 'end')
        self.txt_nombre_conductor.delete(0, 'end')
        self.txt_ci_conductor.delete(0, 'end')
        self.txt_fecha_incautacion.delete(0, 'end')
        self.txt_fiscal_a_cargo.delete(0, 'end')
        self.txt_causa_incautacion.delete(0, 'end')
        
        self.paso_actual = 1
        self.actualizar_flujo()