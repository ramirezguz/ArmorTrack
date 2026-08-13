import customtkinter as ctk

class VentanaLogin(ctk.CTkFrame):
    def __init__(self, parent, autenticador_logica=None, on_login_success=None):
        super().__init__(parent, fg_color="transparent")
        self.parent = parent
        self.logica = autenticador_logica
        self.on_login_success = on_login_success

        self.font_title = ("SF Pro Display", 22, "bold")
        self.font_body = ("SF Pro Text", 13)

        self.crear_componentes()
        
    def crear_componentes(self):
        """Inicializa los campos de texto y botones de autenticacion."""
        self.card = ctk.CTkFrame(self, fg_color="#262626", corner_radius=16, border_width=1, border_color="#333333")
        self.card.pack(fill="both", expand=True, padx=35, pady=35)

        self.logo_label = ctk.CTkLabel(self.card, text="🚘", font=("Arial", 45), anchor="center")
        self.logo_label.pack(pady=(25, 5))

        self.lbl_titulo = ctk.CTkLabel(self.card, text="ARMORTRACK", font=self.font_title, text_color="#FFFFFF")
        self.lbl_titulo.pack(pady=(0, 25))

        self.txt_usuario = ctk.CTkEntry(
            self.card, placeholder_text="Nombre de usuario", font=self.font_body,
            fg_color="#1E1E1E", border_color="#3A3A3A", text_color="#FFFFFF", corner_radius=8, height=40
        )
        self.txt_usuario.pack(fill="x", padx=25, pady=12)
        self.txt_usuario.focus()

        self.txt_password = ctk.CTkEntry(
            self.card, placeholder_text="Contraseña", show="*", font=self.font_body,
            fg_color="#1E1E1E", border_color="#3A3A3A", text_color="#FFFFFF", corner_radius=8, height=40
        )
        self.txt_password.pack(fill="x", padx=25, pady=12)

        self.btn_ingresar = ctk.CTkButton(
            self.card, text="Iniciar Sesión", font=("SF Pro Text", 13, "bold"),
            fg_color="#007AFF", hover_color="#0063CC", text_color="#FFFFFF", corner_radius=8, height=42,
            command=self.procesar_login
        )
        self.btn_ingresar.pack(fill="x", padx=25, pady=(25, 20))

    def procesar_login(self):
        """Valida las credenciales ingresadas."""
        usuario = self.txt_usuario.get().strip()
        password = self.txt_password.get().strip()

        if self.logica:
            exito, mensaje = self.logica.verificar_credenciales(usuario, password)
            if exito and self.on_login_success:
                self.on_login_success()
        else:
            if self.on_login_success:
                self.on_login_success()