import customtkinter as ctk

# 1. Configuración del diseño global
ctk.set_appearance_mode("Dark")       # Modo oscuro
ctk.set_default_color_theme("blue")    # Color de acento base

class MacApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("macOS Premium Interface")
        self.geometry("700x450")
        self.configure(fg_color="#1E1E1E")  # Fondo gris oscuro texturizado

        # Fuentes del sistema Apple
        font_title = ("SF Pro Display", 22, "bold")
        font_body = ("SF Pro Text", 13)

        # -------------------------------------------------------------------------
        # BARRA LATERAL
        # -------------------------------------------------------------------------
        self.sidebar = ctk.CTkFrame(self, width=180, corner_radius=0, fg_color="#161616", border_width=0)
        self.sidebar.pack(side="left", fill="y")

        # Indicador de usuario o logo
        self.user_avatar = ctk.CTkLabel(self.sidebar, text="💻", font=("Arial", 32))
        self.user_avatar.pack(pady=(30, 10))

        self.user_name = ctk.CTkLabel(self.sidebar, text="Admin Panel", font=("SF Pro Text", 14, "bold"), text_color="#A0A0A0")
        self.user_name.pack(pady=(0, 30))

        # Botones de navegación de la barra lateral
        self.btn_nav1 = ctk.CTkButton(self.sidebar, text="Inicio", fg_color="transparent", text_color="#E0E0E0", hover_color="#2A2A2A", font=font_body, anchor="w", height=35)
        self.btn_nav1.pack(fill="x", padx=10, pady=5)

        self.btn_nav2 = ctk.CTkButton(self.sidebar, text="Estadísticas", fg_color="transparent", text_color="#E0E0E0", hover_color="#2A2A2A", font=font_body, anchor="w", height=35)
        self.btn_nav2.pack(fill="x", padx=10, pady=5)

        # -------------------------------------------------------------------------
        # CONTENEDOR PRINCIPAL
        # -------------------------------------------------------------------------
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(side="right", fill="both", expand=True, padx=30, pady=30)

        # Título Principal
        self.title_label = ctk.CTkLabel(self.main_container, text="PANEL DE CONTROL", font=font_title, text_color="#FFFFFF")
        self.title_label.pack(anchor="w", pady=(0, 20))

        # Tarjeta contenedora con esquinas muy redondeadas (Estilo Mac Card)
        self.card = ctk.CTkFrame(self.main_container, fg_color="#262626", corner_radius=16, border_width=1, border_color="#333333")
        self.card.pack(fill="both", expand=True, padx=2, pady=2)

        # -------------------------------------------------------------------------
        # COMPONENTES DENTRO DE LA TARJETA
        # -------------------------------------------------------------------------
        # Texto Informativo
        self.info_label = ctk.CTkLabel(self.card, text="Selecciona una opción del menú dinámico:", font=font_body, text_color="#B0B0B0")
        self.info_label.pack(anchor="w", padx=25, pady=(25, 5))

        # MENÚ DESPLEGABLE MEJORADO
        # Colores vivos, bordes redondeados y tipografía
        self.menu_desplegable = ctk.CTkOptionMenu(
            self.card,
            values=["Producción Activa", "Reporte Mensual", "Ajustes del Sistema", "Cerrar Sesión"],
            font=font_body,
            dropdown_font=font_body,
            fg_color="#007AFF",          # Azul 
            button_color="#0063CC",      # Botón de flecha
            button_hover_color="#0051A8",# Animación
            dropdown_fg_color="#2D2D2D", # Fondo del menú desplegado
            dropdown_hover_color="#007AFF", # Color al pasar el cursor sobre las opciones
            dropdown_text_color="#FFFFFF",
            corner_radius=8,
            height=38
        )
        self.menu_desplegable.pack(fill="x", padx=25, pady=10)

        # Entrada de Texto Estilizada
        self.input_field = ctk.CTkEntry(self.card, placeholder_text="Escribe un comando rápido...", font=font_body, fg_color="#1E1E1E", border_color="#3A3A3A", text_color="#FFFFFF", corner_radius=8, height=38)
        self.input_field.pack(fill="x", padx=25, pady=15)

        # BOTÓN PRINCIPAL ANIMADO 
        # Cambia de color suavemente al pasar el cursor
        self.btn_principal = ctk.CTkButton(
            self.card,
            text="Ejecutar Acción",
            font=("SF Pro Text", 13, "bold"),
            fg_color="#34C759",          # Verde brillante
            hover_color="#28A745",      # Transición de color al pasar el cursor
            text_color="#FFFFFF",
            corner_radius=8,
            height=40,
            command=self.accion_boton
        )
        self.btn_principal.pack(fill="x", padx=25, pady=10)
        self.deiconify()  # Fuerza a la ventana a materializarse
        self.focus()      # Trae la ventana al frente en tu pantalla

    def accion_boton(self):
        seleccion = self.menu_desplegable.get()
        texto = self.input_field.get()
        print(f"Acción ejecutada en: {seleccion}. Entrada: {texto}")



if __name__ == "__main__":
    app = MacApp()
    app.mainloop()



