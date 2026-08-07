import customtkinter as ctk
from Presentation.reportes_vista import VentanaReportes
# Importamos la vista del formulario
from Presentation.formulario_vehiculo import FormularioVehiculo
from PIL import Image


class VentanaMenuPrincipal(ctk.CTkFrame):
    def __init__(self, root, autenticador_logica=None, on_logout=None):
        super().__init__(root, fg_color="transparent")
        self.root = root
        self.logica = autenticador_logica
        self.on_logout = on_logout

        # Configuración de columnas (sidebar fija + área central expandible)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.crear_componentes()

    def crear_componentes(self):
        # --- 1. BARRA LATERAL (NAVBAR) ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)  # Empuja el botón de cerrar sesión abajo

        # Título / Logo
        lbl_logo = ctk.CTkLabel(
            self.sidebar, 
            text="🚘" "ARMORTRACK", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        lbl_logo.grid(row=0, column=0, padx=20, pady=(20, 25))

        # --- BOTONES DE NAVEGACIÓN ---
        btn_inicio = ctk.CTkButton(
            self.sidebar, text="🏠 Inicio", command=self.mostrar_inicio
        )
        btn_inicio.grid(row=1, column=0, padx=20, pady=8)

        btn_ingresar = ctk.CTkButton(
            self.sidebar, text="🚗 Ingresar / Incautar", command=self.mostrar_ingreso
        )
        btn_ingresar.grid(row=2, column=0, padx=20, pady=8)

        btn_entregar = ctk.CTkButton(
            self.sidebar, text="📋 Entregar Vehículo", command=self.mostrar_entrega
        )
        btn_entregar.grid(row=3, column=0, padx=20, pady=8)

        btn_reportes = ctk.CTkButton(
            self.sidebar, text="📊 Reportes / Consultas", command=self.mostrar_reportes
        )
        btn_reportes.grid(row=4, column=0, padx=20, pady=8)

        # Botón Cerrar Sesión
        btn_logout = ctk.CTkButton(
            self.sidebar, 
            text="Cerrar Sesión", 
            fg_color="#D32F2F", 
            hover_color="#B71C1C",
            command=self.cerrar_sesion
        )
        btn_logout.grid(row=7, column=0, padx=20, pady=20)

        # --- 2. CONTENEDOR PRINCIPAL (ÁREA DE TRABAJO) ---
        self.area_contenido = ctk.CTkFrame(self, fg_color="transparent")
        self.area_contenido.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.area_contenido.grid_columnconfigure(0, weight=1)
        self.area_contenido.grid_rowconfigure(0, weight=1)

        # Vista inicial por defecto
        self.mostrar_inicio()

    def limpiar_contenido(self):
        """Limpia la pantalla central para cambiar de opción."""
        for widget in self.area_contenido.winfo_children():
            widget.destroy()

    def mostrar_inicio(self):
        self.limpiar_contenido()
        lbl_bienvenida = ctk.CTkLabel(
            self.area_contenido, 
            text="Bienvenido al Sistema ArmorTrack", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        lbl_bienvenida.pack(pady=40)

        img_logo = ctk.CTkImage(
        light_image=Image.open("Imagenes/logo.png"),
        dark_image=Image.open("Imagenes/logo.png"),
        size=(550, 600) # Ajusta el tamaño (ancho, alto) en píxeles
    )

    # Se usa un CTkLabel vacío (sin texto) para contener la imagen
        lbl_imagen = ctk.CTkLabel(self.area_contenido, image=img_logo, text="")
        lbl_imagen.pack(pady=20)

    def mostrar_ingreso(self):
        self.limpiar_contenido()
        # Carga el formulario de registro/incautación de vehículos
        if hasattr(FormularioVehiculo, "FormularioVehiculo"):
            vista_ingreso = FormularioVehiculo.FormularioVehiculo(self.area_contenido, self.logica)
        else:
            vista_ingreso = FormularioVehiculo(self.area_contenido, self.logica)
        vista_ingreso.pack(fill="both", expand=True)

    def mostrar_entrega(self):
        self.limpiar_contenido()
        # Si tienes una vista específica para entrega (ej: SalidaVehiculo), instánciala aquí.
        lbl_temp = ctk.CTkLabel(
            self.area_contenido, 
            text="Módulo de Salida / Entrega de Vehículos", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        lbl_temp.pack(pady=40)

    def mostrar_reportes(self):
        self.limpiar_contenido()
        vista_reportes = VentanaReportes(self.area_contenido, self.logica)
        vista_reportes.pack(fill="both", expand=True)

    def cerrar_sesion(self):
        if self.on_logout:
            self.on_logout()