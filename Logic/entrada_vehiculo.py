import json

class RegistroEntrada:
    def __init__(self):
        self.datos_motos = {}
        self.datos_vehiculos = {}
        self.cargar_datos_predefinidos()

    def cargar_datos_predefinidos(self):
        try:
            with open("Database/motocicletas.json", "r", encoding="utf-8") as f:
                self.datos_motos = json.load(f)
        except FileNotFoundError:
            print("Aviso: No se encontró motocicletas.json")

        try:
            with open("Database/vehiculos.json", "r", encoding="utf-8") as f:
                self.datos_vehiculos = json.load(f)
        except FileNotFoundError:
            print("Aviso: No se encontró vehiculos.json")

    def obtener_marcas_por_tipo(self, tipo):
        """Devuelve las marcas del JSON y añade 'OTRO' al final."""
        marcas = []
        if tipo == "MOTOCICLETA":
            marcas = list(self.datos_motos.keys())
        elif tipo == "VEHÍCULO":
            marcas = list(self.datos_vehiculos.keys())
        marcas.append("OTRO")
        return marcas

    def obtener_modelos_por_marca_y_tipo(self, tipo, marca):
        """Devuelve los modelos de la marca y añade 'OTRO' al final."""
        if marca == "OTRO":
            return ["OTRO"]
        marca_upper = marca.upper()
        modelos = []
        if tipo == "MOTOCICLETA":
            modelos = list(self.datos_motos.get(marca_upper, []))
        elif tipo == "VEHÍCULO":
            modelos = list(self.datos_vehiculos.get(marca_upper, []))
        modelos.append("OTRO")
        return modelos

    def validar_ingreso(self, tipo, subcategoria, matricula, marca, marca_manual, modelo, modelo_manual, anio, color):
        """Valida los datos considerando si son predefinidos o escritos a mano."""
        if not tipo or tipo == "Seleccionar...":
            return False, "Debe seleccionar el Tipo (Motocicleta o Vehículo)."
        if tipo == "VEHÍCULO" and not subcategoria:
            return False, "Debe seleccionar una subcategoría para el Vehículo."
        if not matricula:
            return False, "La matrícula es obligatoria."
        if not color:
            return False, "Debe seleccionar un color."
        if not anio or not anio.isdigit():
            return False, "El año debe ser un número válido."

        final_marca = marca_manual.strip() if marca == "OTRO" else marca
        if not final_marca:
            return False, "Debe especificar la marca del vehículo."

        final_modelo = modelo_manual.strip() if modelo == "OTRO" else modelo
        if not final_modelo:
            return False, "Debe especificar el modelo del vehículo."

        return True, "Datos válidos."

    def obtener_vehiculos_por_estado(self, estado_filtro):
        """Filtra la lista de vehículos históricos de acuerdo al estado solicitado."""
        inventario_historico = [
            {"tipo": "VEHÍCULO", "subcategoria": "AUTOMÓVIL", "matricula": "AAA123", "marca": "TOYOTA", "modelo": "COROLLA", "anio": "2015", "color": "BLANCO", "estado": "INCAUTADO"},
            {"tipo": "MOTOCICLETA", "subcategoria": "", "matricula": "777XYZ", "marca": "HONDA", "modelo": "NAVI", "anio": "2022", "color": "ROJO", "estado": "DEPOSITADO"},
            {"tipo": "VEHÍCULO", "subcategoria": "CAMIÓN", "matricula": "BBB456", "marca": "VOLVO", "modelo": "FH", "anio": "2018", "color": "GRIS", "estado": "ENTREGADO"},
            {"tipo": "MOTOCICLETA", "subcategoria": "", "matricula": "SIN MATRÍCULA", "marca": "KENTON", "modelo": "BLITZ", "anio": "2021", "color": "NEGRO", "estado": "INCAUTADO"}
        ]
        if estado_filtro == "TODOS":
            return inventario_historico
        return [v for v in inventario_historico if v["estado"] == estado_filtro]
