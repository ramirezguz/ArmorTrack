import customtkinter as ctk
from Presentation.login_vista import VentanaLogin
from Presentation.menu_vista import VentanaMenuPrincipal
from Logic.logica_inventario import InventarioLogica

# Configuración global de CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ARMORTRACK")
        self.geometry("450x550")
        self.resizable(False, False)

        self.inventario_logica = InventarioLogica()

        # Marco contenedor para alternar entre Login y Menú
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        # Iniciar mostrando la pantalla de Login
        self.mostrar_login()
        self.attributes("-topmost", True)
        self.attributes("-topmost", False)
        self.focus_force()

    def mostrar_login(self):
        self.limpiar_pantalla()
        
        # Ajustamos tamaño para la ventana de login
        self.geometry("450x550")
        self.resizable(False, False)

        # Instanciamos el login pasando la función para avanzar al éxito
        self.vista_login = VentanaLogin(
            self.container, 
            autenticador_logica=None, 
            on_login_success=self.mostrar_dashboard
        )
        self.vista_login.pack(fill="both", expand=True)

    def mostrar_dashboard(self):
        self.limpiar_pantalla()

        # Ajustamos tamaño para el menú principal
        self.geometry("1000x650")
        self.resizable(True, True)


        # Instanciamos el menú principal pasando la función para cerrar sesión
        self.vista_menu = VentanaMenuPrincipal(
            self.container, 
            autenticador_logica= self.inventario_logica, # Pasamos la instancia aquí
            on_logout=self.mostrar_login
        )
        self.vista_menu.pack(fill="both", expand=True)

    def limpiar_pantalla(self):
        for widget in self.container.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = App()
    app.focus_force()
    app.mainloop()