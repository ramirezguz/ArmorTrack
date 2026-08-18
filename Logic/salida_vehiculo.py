import sqlite3
import os

class SalidaVehiculoLogica:
    def __init__(self, ruta_db=None):
        if ruta_db:
            self.ruta_db = ruta_db
        else:
            self.ruta_db = os.path.join(os.path.dirname(__file__), "..", "Database", "inventario.db")

    def _conectar(self):
        """Establece la conexión con la base de datos SQLite."""
        conn = sqlite3.connect(self.ruta_db)
        conn.row_factory = sqlite3.Row
        return conn

    def buscar_para_entrega(self, criterio: str):
        try:
            with self._conectar() as conn:
                cursor = conn.cursor()
                term = f"%{criterio.strip().upper()}%"
                query = """
                    SELECT id, tipo, marca, modelo, matricula, chasis, estado 
                    FROM vehiculos_datos 
                    WHERE (UPPER(matricula) LIKE ? OR UPPER(chasis) LIKE ?) 
                    AND estado IN ('INCAUTADO', 'DEPOSITADO')
                """
                cursor.execute(query, (term, term))
                filas = cursor.fetchall()
                return [dict(f) for f in filas] if filas else []
        except Exception as e:
            print(f"[ERROR BUSQUEDA]: {e}")
            return []

    def procesar_egreso(self, vehiculo_id: int, datos: dict):
        """Modifica el estado del vehículo a ENTREGADO y concatena el historial del oficio."""
        try:
            with self._conectar() as conn:
                cursor = conn.cursor()
                
                cursor.execute("UPDATE vehiculos_datos SET estado = 'ENTREGADO' WHERE id = ?", (vehiculo_id,))
                
                oficio = datos.get("oficio", "").strip().upper()
                beneficiario = datos.get("nombre_recibe", "").strip().upper()
                ci = datos.get("ci_recibe", "").strip()
                fecha = datos.get("fecha_entrega", "")
                
                historial = f"\n[ENTREGADO] Oficio N°: {oficio} | Retirado por: {beneficiario} (CI: {ci}) el {fecha}"
                
                cursor.execute("""
                    UPDATE datos_judiciales 
                    SET causa_incautacion = causa_incautacion || ? 
                    WHERE vehiculo_id = ?
                """, (historial, vehiculo_id))
                
                conn.commit()
                return True, "Vehículo liberado correctamente en el sistema."
        except Exception as e:
            print(f"[ERROR CRÍTICO EGRESO]: {e}")
            return False, str(e)