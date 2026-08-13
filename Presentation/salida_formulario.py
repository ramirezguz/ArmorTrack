import customtkinter as ctk
from datetime import datetime
from Logic.salida_vehiculo import SalidaVehiculoLogica

class FormularioSalida(ctk.CTkFrame):
    def __init__(self, parent, logica_inventario=None):
        super().__init__(parent, fg_color="transparent")
        
        self.logica_salida = SalidaVehiculoLogica()
        self.vehiculo_encontrado = None

        lbl_titulo = ctk.CTkLabel(self, text="MÓDULO DE SALIDA / ENTREGA DE VEHÍCULOS", font=ctk.CTkFont(size=20, weight="bold"))
        lbl_titulo.pack(pady=(20, 10))

        frame_busqueda = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=10)
        frame_busqueda.pack(fill="x", padx=30, pady=10)

        lbl_buscar = ctk.CTkLabel(frame_busqueda, text="Buscar por Matrícula o Chasis:", font=ctk.CTkFont(size=14, weight="bold"))
        lbl_buscar.pack(side="left", padx=15, pady=15)

        self.txt_buscar = ctk.CTkEntry(frame_busqueda, placeholder_text="Ej: AAIE123 o 456PRUEBA...", width=300, height=35)
        self.txt_buscar.pack(side="left", padx=10, pady=15)
        self.txt_buscar.bind("<Return>", lambda e: self.ejecutar_busqueda())

        btn_buscar = ctk.CTkButton(
            frame_busqueda, text="🔍 Buscar Rodado", command=self.ejecutar_busqueda,
            fg_color="#2196F3", hover_color="#1976D2", height=35, font=ctk.CTkFont(weight="bold")
        )
        btn_buscar.pack(side="left", padx=15, pady=15)

        self.frame_formulario = ctk.CTkScrollableFrame(self, fg_color="#1e1e1e", corner_radius=10)
        
        self.lbl_estado = ctk.CTkLabel(
            self, text="Ingrese una matrícula o chasis activo para comenzar.", 
            font=ctk.CTkFont(size=14, slant="italic"), text_color="gray"
        )

    def ejecutar_busqueda(self):
        """Consulta la existencia del vehiculo segun los parametros de busqueda."""
        criterio = self.txt_buscar.get().strip()
        if not criterio:
            self.lbl_estado.configure(text="⚠️ Por favor, ingrese un criterio de búsqueda.", text_color="#FFCC00")
            self.frame_formulario.pack_forget()
            return

        vehiculo = self.logica_salida.buscar_para_entrega(criterio)

        if vehiculo:
            self.vehiculo_encontrado = vehiculo
            self.lbl_estado.pack_forget()
            self.mostrar_formulario_entrega()
        else:
            self.vehiculo_encontrado = None
            self.lbl_estado.configure(
                text=f"❌ No se encontró ningún vehículo ACTIVO (Incautado/Depositado) con el criterio: '{criterio}'", 
                text_color="#FF3333"
            )
            self.frame_formulario.pack_forget()

    def mostrar_formulario_entrega(self):
        """Inicializa los campos para registrar los datos de entrega."""
        for widget in self.frame_formulario.winfo_children():
            widget.destroy()

        v = self.vehiculo_encontrado
        self.frame_formulario.pack(fill="both", expand=True, padx=30, pady=10)

        lbl_sub1 = ctk.CTkLabel(self.frame_formulario, text="📄 DATOS DEL RODADO A ENTREGAR", font=ctk.CTkFont(size=14, weight="bold"), text_color="#2196F3")
        lbl_sub1.pack(anchor="w", padx=20, pady=(10, 5))

        grid_datos = ctk.CTkFrame(self.frame_formulario, fg_color="transparent")
        grid_datos.pack(fill="x", padx=20, pady=5)

        detalles = f"Tipo: {v['tipo']}  |  Marca: {v['marca']}  |  Modelo: {v['modelo']}\nMatrícula: {v['matricula']}  |  Chasis: {v['chasis']}  |  Estado Actual: {v['estado']}"
        lbl_detalles = ctk.CTkLabel(grid_datos, text=detalles, font=ctk.CTkFont(size=13), justify="left", anchor="w")
        lbl_detalles.pack(fill="x", pady=5)

        ctk.CTkLabel(self.frame_formulario, text="─"*80, text_color="#333333").pack(pady=5)

        lbl_sub2 = ctk.CTkLabel(self.frame_formulario, text="⚖️ DATOS DE OFICIO JUDICIAL A ENTREGAR", font=ctk.CTkFont(size=14, weight="bold"), text_color="#4CAF50")
        lbl_sub2.pack(anchor="w", padx=20, pady=(5, 10))

        ctk.CTkLabel(self.frame_formulario, text="N° de Oficio Judicial/Fiscal", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20)
        self.txt_oficio = ctk.CTkEntry(self.frame_formulario, placeholder_text="Ej: OFICIO N° 124/2026", width=500)
        self.txt_oficio.pack(anchor="w", padx=20, pady=(0, 15))

        ctk.CTkLabel(self.frame_formulario, text="fecha del Oficio Judicial/Fiscal:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20)
        self.txt_fecha = ctk.CTkEntry(self.frame_formulario, placeholder_text="Ej: 01/01/2026", width=500)
        self.txt_fecha.pack(anchor="w", padx=20, pady=(0, 15))        

        ctk.CTkLabel(self.frame_formulario, text="Nombre Completo de la Persona que Retira:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20)
        self.txt_recibe = ctk.CTkEntry(self.frame_formulario, placeholder_text="Ej: JUAN PÉREZ GÓMEZ", width=500)
        self.txt_recibe.pack(anchor="w", padx=20, pady=(0, 15))

        ctk.CTkLabel(self.frame_formulario, text="FIRMADO POR:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20)
        self.txt_firma = ctk.CTkEntry(self.frame_formulario, placeholder_text="Ej: Abg. JUAN PEREZ", width=500)
        self.txt_firma.pack(anchor="w", padx=20, pady=(0, 15))

        ctk.CTkLabel(self.frame_formulario, text="N° de C.I. de la Persona que Retira:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20)
        self.txt_ci = ctk.CTkEntry(self.frame_formulario, placeholder_text="Ej: 1234567", width=500)
        self.txt_ci.pack(anchor="w", padx=20, pady=(0, 15))

        lbl_sub3 = ctk.CTkLabel(self.frame_formulario, text="👮 DATOS DEL OFICIAL DE GUARDIA", font=ctk.CTkFont(size=14, weight="bold"), text_color="#4CAF50")
        lbl_sub3.pack(anchor="w", padx=20, pady=(5, 10))

        ctk.CTkLabel(self.frame_formulario, text="OFICIAL DE GUARDIA:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20)
        self.txt_oficial = ctk.CTkEntry(self.frame_formulario, placeholder_text="OFIC. O SUBOFICIAL JUAN PEREZ....", width=500)
        self.txt_oficial.pack(anchor="w", padx=20, pady=(0, 15))

        btn_finalizar = ctk.CTkButton(
            self.frame_formulario, text="💾 Procesar y Registrar Salida", command=self.confirmar_entrega,
            fg_color="#4CAF50", hover_color="#45a049", height=40, font=ctk.CTkFont(size=14, weight="bold")
        )
        btn_finalizar.pack(pady=25)

    def confirmar_entrega(self):
        """Valida y envia los datos de egreso del vehiculo."""
        oficio = self.txt_oficio.get().strip()
        fecha = self.txt_fecha.get().strip()
        recibe = self.txt_recibe.get().strip()
        firma = self.txt_firma.get().strip()
        ci = self.txt_ci.get().strip()
        oficial = self.txt_oficial.get().strip()

        if not oficio or not recibe or not ci:
            from tkinter import messagebox
            messagebox.showwarning("Campos Incompletos", "Por favor, complete todos los campos de la orden de liberación.")
            return

        datos_entrega = {
            "oficio": oficio,
            "fecha": fecha,
            "nombre_recibe": recibe,
            "firma": firma,
            "ci_recibe": ci,
            "oficial": oficial,
            "fecha_entrega": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }

        exito, msg = self.logica_salida.procesar_egreso(self.vehiculo_encontrado["id"], datos_entrega)

        from tkinter import messagebox
        if exito:
            messagebox.showinfo("Éxito", msg)
            self.txt_buscar.delete(0, "end")
            self.frame_formulario.pack_forget()
            self.lbl_estado.configure(text="✅ Entrega procesada correctamente. Ingrese otro rodado si lo desea.", text_color="#4CAF50")
            self.lbl_estado.pack(pady=40)
        else:
            messagebox.showerror("Error", f"No se pudo guardar la entrega:\n{msg}")