from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

# Importamos las clases de la capa de lógica
from Logic.logica_inventario import InventarioLogica
from Logic.salida_vehiculo import SalidaVehiculoLogica

app = FastAPI(title="ARMORTRACK API")

# Configuración de CORS para permitir solicitudes desde el Frontend (React + Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancias globales de la capa lógica
logica_inv = InventarioLogica()
logica_sal = SalidaVehiculoLogica()


# ==========================================
# 1. ENDPOINT: ESTADÍSTICAS DEL DASHBOARD
# ==========================================
@app.get("/api/v1/estadisticas")
def obtener_estadisticas():
    try:
        return logica_inv.obtener_estadisticas_totales()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas: {str(e)}")


# ==========================================
# 2. ENDPOINT: BUSCADOR / INVENTARIO / REPORTES
# ==========================================
@app.get("/api/v1/vehiculos/buscar")
def buscar_vehiculos(criterio: str = Query("", description="Criterio de búsqueda por chapa, marca, conductor, etc.")):
    try:
        # Busca vehículos retenidos o que coincidan con el criterio para entrega o consulta
        resultados = logica_sal.buscar_para_entrega(criterio)
        return resultados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar vehículos: {str(e)}")


# ==========================================
# 3. ENDPOINT: OBTENER VEHÍCULO POR ID
# ==========================================
@app.get("/api/v1/vehiculos/{id}")
def obtener_vehiculo_por_id(id: str):
    try:
        vehiculo = logica_sal.obtener_por_id(id)
        if not vehiculo:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")
        return vehiculo
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener vehículo: {str(e)}")


# ==========================================
# 4. ENDPOINT: REGISTRAR / INCAUTAR VEHÍCULO
# ==========================================
@app.post("/api/v1/vehiculos")
def registrar_vehiculo(datos: dict):
    try:
        exito, mensaje = logica_inv.registrar_vehiculo(datos)
        if not exito:
            raise HTTPException(status_code=400, detail=mensaje)
        return {"mensaje": mensaje}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al registrar vehículo: {str(e)}")


# ==========================================
# 5. ENDPOINT: REGISTRAR SALIDA / LIBERACIÓN
# ==========================================
@app.post("/api/v1/salidas")
def registrar_salida_vehiculo(datos: dict):
    try:
        exito, mensaje = logica_sal.registrar_salida(datos)
        if not exito:
            raise HTTPException(status_code=400, detail=mensaje)
        return {"mensaje": mensaje}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al registrar la salida: {str(e)}")


import customtkinter as ctk
from Presentation.login_vista import VentanaLogin
from Presentation.menu_vista import VentanaMenuPrincipal
from Logic.logica_inventario import InventarioLogica

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