import json

class Autenticador:
    def __init__(self):
        self.usuario_actual = None
        self.rol_actual = None

    def verificar_credenciales(self, usuario_ingresado, password_ingresado):
        """Valida las credenciales comparándolas con el archivo usuarios.json."""
        if not usuario_ingresado or not password_ingresado:
            return False, "Por favor, complete todos los campos."
        try:
            with open("Database/usuarios.json", "r", encoding="utf-8") as archivo:
                usuarios = json.load(archivo)
                for u in usuarios:
                    if u["usuario"] == usuario_ingresado and u["password"] == password_ingresado:
                        self.usuario_actual = u["usuario"]
                        self.rol_actual = u["rol"]
                        return True, "Credenciales correctas."
            return False, "Usuario o contraseña incorrectos."
        except FileNotFoundError:
            return False, "Error crítico: No se encontró el archivo de base de datos de usuarios."
        except json.JSONDecodeError:
            return False, "Error crítico: El archivo de usuarios tiene un formato JSON inválido."
