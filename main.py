import customtkinter as ctk
from Presentation.ventana_login import VentanaLogin
from Presentation.ventana_menu_principal import VentanaMenuPrincipal
from Logic.inventario_logica import InventarioLogica

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ARMORTRACK")
        self.geometry("450x550")
        self.resizable(False, False)

        self.inventario_logica = InventarioLogica()

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.mostrar_login()
        self.attributes("-topmost", True)
        self.attributes("-topmost", False)
        self.focus_force()

    def mostrar_login(self):
        """Configura las dimensiones de la ventana y monta el modulo de autenticacion."""
        self.limpiar_pantalla()
        
        ancho_ventana = 450
        alto_ventana = 550

        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()

        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)

        self.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        self.resizable(False, False)

        self.vista_login = VentanaLogin(
            self.container, 
            autenticador_logica=None, 
            on_login_success=self.mostrar_dashboard
        )
        self.vista_login.pack(fill="both", expand=True)

    def mostrar_dashboard(self):
        """Redimensiona la ventana y monta el entorno del menu principal."""
        self.limpiar_pantalla()

        self.geometry("1000x650")
        self.resizable(True, True)

        self.vista_menu = VentanaMenuPrincipal(
            self.container, 
            autenticador_logica=self.inventario_logica,
            on_logout=self.mostrar_login
        )
        self.vista_menu.pack(fill="both", expand=True)

    def limpiar_pantalla(self):
        """Elimina todos los widgets secundarios del contenedor principal."""
        for widget in self.container.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = App()
    app.focus_force()
    app.mainloop()