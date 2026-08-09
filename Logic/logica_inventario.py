import sqlite3
import os

class InventarioLogica:
    def __init__(self):
        # Apuntamos al nuevo archivo .db
        self.ruta_bd = os.path.join(os.path.dirname(__file__), "..", "Database", "inventario.db")

    def _conectar(self):
        """Helper para obtener una conexión rápida a la BD."""
        return sqlite3.connect(self.ruta_bd)

    def registrar_vehiculo(self, datos):
        """Inserta un nuevo vehículo en la base de datos."""
        sql = """
        INSERT INTO vehiculos (
            estado, tipo, subcategoria, marca, modelo, color, 
            matricula, chasis, inscripto_nombre, ci_num, unidad_a_cargo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        try:
            with self._conectar() as conexion:
                cursor = conexion.cursor()
                cursor.execute(sql, (
                    datos.get("estado"),
                    datos.get("tipo"),
                    datos.get("subcategoria"),
                    datos.get("marca"),
                    datos.get("modelo"),
                    datos.get("color"),
                    datos.get("Matricula"),
                    datos.get("chasis"),
                    datos.get("Inscripto a Nombre de"),
                    datos.get("C_I_N°"),
                    datos.get("unidad_a_cargo")
                ))
                conexion.commit()
            return True, "Vehículo registrado correctamente en SQLite."
        except sqlite3.IntegrityError:
            return False, "Error: La matrícula ya se encuentra registrada."
        except Exception as e:
            return False, f"Error en la base de datos: {str(e)}"

    def buscar_vehiculos(self, termino):
        """Busca vehículos por matrícula o chasis usando coincidencia parcial (LIKE)."""
        # Si el buscador está vacío, traemos los últimos 50 registros por defecto
        if not termino.strip():
            sql = "SELECT * FROM vehiculos ORDER BY id DESC LIMIT 50"
            parametros = ()
        else:
            # Buscamos coincidencias aproximadas (ej: 'ABC' encontrará 'ABC123')
            sql = """
            SELECT * FROM vehiculos 
            WHERE matricula LIKE ? OR chasis LIKE ?
            ORDER BY id DESC
            """
            parametros = (f"%{termino}%", f"%{termino}%")

        try:
            with self._conectar() as conexion:

                conexion.row_factory = sqlite3.Row
                cursor = conexion.cursor()
                cursor.execute(sql, parametros)
                
                # Convertimos los resultados a una lista de diccionarios estándar
                resultados = [dict(row) for row in cursor.fetchall()]
                return resultados
        except Exception as e:
            print(f"Error al realizar la búsqueda: {e}")
            return []
        
    def obtener_estadisticas_totales(self):
        """Devuelve la cantidad total de registros, vehículos y motocicletas."""
        sql_total = "SELECT COUNT(*) FROM vehiculos"
        sql_vehiculos = "SELECT COUNT(*) FROM vehiculos WHERE UPPER(tipo) = 'VEHÍCULO' OR UPPER(tipo) = 'VEHICULO'"
        sql_motos = "SELECT COUNT(*) FROM vehiculos WHERE UPPER(tipo) = 'MOTOCICLETA' OR UPPER(tipo) = 'MOTO'"
        
        stats = {"total": 0, "vehiculos": 0, "motos": 0}
        
        try:
            with self._conectar() as conexion:
                cursor = conexion.cursor()
                
                # Contar Total
                cursor.execute(sql_total)
                stats["total"] = cursor.fetchone()[0]
                
                # Contar Vehículos
                cursor.execute(sql_vehiculos)
                stats["vehiculos"] = cursor.fetchone()[0]
                
                # Contar Motos
                cursor.execute(sql_motos)
                stats["motos"] = cursor.fetchone()[0]
                
        except Exception as e:
            print(f"Error al obtener estadísticas de la BD: {e}")
            
        return stats