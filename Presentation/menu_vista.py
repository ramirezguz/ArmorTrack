import customtkinter as ctk
from Presentation.reportes_vista import VentanaReportes
from Presentation.formulario_vehiculo import FormularioVehiculo
from PIL import Image

class VentanaMenuPrincipal(ctk.CTkFrame):
    def __init__(self, root, autenticador_logica=None, on_logout=None):
        super().__init__(root, fg_color="transparent")
        self.root = root
        self.logica = autenticador_logica
        self.on_logout = on_logout

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.crear_componentes()

    def crear_componentes(self):
        """Inicializa los componentes de navegacion lateral y contenedor principal."""
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)

        lbl_logo = ctk.CTkLabel(self.sidebar, text="🚘 ARMORTRACK", font=ctk.CTkFont(size=18, weight="bold"))
        lbl_logo.grid(row=0, column=0, padx=20, pady=(20, 25))

        btn_inicio = ctk.CTkButton(self.sidebar, text="🏠 Inicio", command=self.mostrar_inicio)
        btn_inicio.grid(row=1, column=0, padx=20, pady=8)

        btn_ingresar = ctk.CTkButton(self.sidebar, text="🚗 Ingresar / Incautar", command=self.mostrar_ingreso)
        btn_ingresar.grid(row=2, column=0, padx=20, pady=8)

        btn_entregar = ctk.CTkButton(self.sidebar, text="📋 Entregar Vehículo", command=self.mostrar_entrega)
        btn_entregar.grid(row=3, column=0, padx=20, pady=8)

        btn_reportes = ctk.CTkButton(self.sidebar, text="📊 Reportes / Consultas", command=self.mostrar_reportes)
        btn_reportes.grid(row=4, column=0, padx=20, pady=8)

        btn_logout = ctk.CTkButton(
            self.sidebar, text="Cerrar Sesión", fg_color="#D32F2F", hover_color="#B71C1C", command=self.cerrar_sesion
        )
        btn_logout.grid(row=7, column=0, padx=20, pady=20)

        self.area_contenido = ctk.CTkFrame(self, fg_color="transparent")
        self.area_contenido.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.area_contenido.grid_columnconfigure(0, weight=1)
        self.area_contenido.grid_rowconfigure(0, weight=1)

        self.mostrar_inicio()

    def limpiar_contenido(self):
        """Remueve los componentes del contenedor central."""
        for widget in self.area_contenido.winfo_children():
            widget.destroy()

    def mostrar_inicio(self):
        """Muestra la interfaz de bienvenida."""
        self.limpiar_contenido()
        lbl_bienvenida = ctk.CTkLabel(
            self.area_contenido, text="Bienvenido al Sistema ArmorTrack", font=ctk.CTkFont(size=22, weight="bold")
        )
        lbl_bienvenida.pack(pady=40)

        img_logo = ctk.CTkImage(
            light_image=Image.open("Imagenes/logo.png"),
            dark_image=Image.open("Imagenes/logo.png"),
            size=(550, 600)
        )

        lbl_imagen = ctk.CTkLabel(self.area_contenido, image=img_logo, text="")
        lbl_imagen.pack(pady=20)

    def mostrar_ingreso(self):
        """Muestra el formulario de registro de vehiculos."""
        self.limpiar_contenido()
        if hasattr(FormularioVehiculo, "FormularioVehiculo"):
            vista_ingreso = FormularioVehiculo.FormularioVehiculo(self.area_contenido, self.logica)
        else:
            vista_ingreso = FormularioVehiculo(self.area_contenido, self.logica)
        vista_ingreso.pack(fill="both", expand=True)

    def mostrar_entrega(self):
        """Muestra el formulario de salida de vehiculos."""
        self.limpiar_contenido()
        from Presentation.salida_formulario import FormularioSalida
        vista_salida = FormularioSalida(self.area_contenido)
        vista_salida.pack(fill="both", expand=True)

    def mostrar_reportes(self):
        """Muestra la vista de reportes."""
        self.limpiar_contenido()
        vista_reportes = VentanaReportes(self.area_contenido, self.logica)
        vista_reportes.pack(fill="both", expand=True)

    def cerrar_sesion(self):
        """Ejecuta la rutina de cierre de sesion."""
        if self.on_logout:
            self.on_logout()