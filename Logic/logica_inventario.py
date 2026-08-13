import sqlite3
import os
import datetime

class InventarioLogica:
    def __init__(self):
        self.ruta_db = os.path.join(os.path.dirname(__file__), "..", "Database", "inventario.db")

    def _conectar(self):
        """Establece la conexión con la base de datos SQLite y configura el row_factory."""
        conn = sqlite3.connect(self.ruta_db)
        conn.row_factory = sqlite3.Row
        return conn

    def obtener_estadisticas_totales(self):
        """Ejecuta los conteos globales y por tipo en la tabla de vehículos."""
        try:
            with self._conectar() as conn:
                cursor = conn.cursor()
                
                cursor.execute("SELECT COUNT(*) FROM vehiculos_datos")
                total = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM vehiculos_datos WHERE UPPER(tipo) = 'VEHÍCULO'")
                vehiculos = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM vehiculos_datos WHERE UPPER(tipo) = 'MOTOCICLETA'")
                motos = cursor.fetchone()[0]
                
                return {"total": total, "vehiculos": vehiculos, "motos": motos}
        except Exception as e:
            print(f"[ERROR BD ESTADISTICAS]: {e}")
            return {"total": 0, "vehiculos": 0, "motos": 0}

    def buscar_vehiculos(self, criterio: str):
        """Realiza una consulta con LEFT JOIN filtrando por los campos clave si existe criterio."""
        try:
            with self._conectar() as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT 
                        v.id, v.tipo, v.subcategoria, v.estado, v.marca, v.modelo, v.color, 
                        v.ano_vehiculo, v.matricula, v.chasis, v.inscripto_nombre, v.ci_num,
                        c.nombre_completo AS nombre_conductor, c.ci_num AS ci_conductor,
                        j.unidad_fiscal AS unidad_a_cargo, j.fecha_incautacion, 
                        j.fiscal_a_cargo, j.causa_incautacion
                    FROM vehiculos_datos v
                    LEFT JOIN datos_judiciales j ON v.id = j.vehiculo_id
                    LEFT JOIN conductores c ON j.conductor_id = c.id
                """
                
                if criterio:
                    query += """
                        WHERE v.matricula LIKE ? 
                           OR v.chasis LIKE ? 
                           OR v.marca LIKE ? 
                           OR c.nombre_completo LIKE ? 
                           OR j.unidad_fiscal LIKE ?
                    """
                    param = f"%{criterio}%"
                    cursor.execute(query, (param, param, param, param, param))
                else:
                    cursor.execute(query)
                
                resultados = []
                for row in cursor.fetchall():
                    resultados.append(dict(row))
                    
                return resultados
                
        except Exception as e:
            print(f"[ERROR BD BUSQUEDA]: {e}")
            return []

    def registrar_vehiculo(self, datos: dict):
        """Inserta los datos del formulario de manera relacional en las tres tablas correspondientes."""
        try:
            matricula = datos.get("Matricula", datos.get("matricula", "")).strip().upper()
            chasis = datos.get("chasis", "").strip().upper()
            
            if not matricula and not chasis:
                marca_tiempo = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
                matricula = f"S-M-{marca_tiempo}"
                chasis = f"S-C-{marca_tiempo}"
                
                nota_anonimo = " [ALERTA: Ingresado sin Chapa ni Chasis por falta de visibilidad]"
                datos["causa_incautacion"] = datos.get("causa_incautacion", "").strip() + nota_anonimo

            tipo = datos.get("tipo", "VEHÍCULO").strip().upper()
            subcategoria = datos.get("subcategoria", "DESCONOCIDO").strip().upper()
            estado = datos.get("estado", "INCAUTADO").strip().upper()
            marca = datos.get("marca", "").strip().upper() or "DESCONOCIDA"
            modelo = datos.get("modelo", "").strip().upper() or "DESCONOCIDO"
            color = datos.get("color", "").strip().upper() or "INDETERMINADO"
            ano_vehiculo = datos.get("ano_vehiculo", "").strip() or "N/A"
            inscripto_nombre = datos.get("Inscripto a Nombre de", datos.get("inscripto_nombre", "")).strip().upper() or "NO IDENTIFICADO"
            ci_num = datos.get("C_I_N°", datos.get("ci_num", "")).strip() or "N/A"

            with self._conectar() as conn:
                cursor = conn.cursor()
                
                query_v = """
                    INSERT INTO vehiculos_datos 
                    (estado, tipo, subcategoria, marca, modelo, color, ano_vehiculo, matricula, chasis, inscripto_nombre, ci_num) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                cursor.execute(query_v, (estado, tipo, subcategoria, marca, modelo, color, ano_vehiculo, matricula, chasis, inscripto_nombre, ci_num))
                vehiculo_id = cursor.lastrowid

                nombre_conductor = datos.get("nombre_conductor", "").strip().upper() or "DESCONOCIDO / NO IDENTIFICADO"
                ci_conductor = datos.get("ci_conductor", "").strip() or "N/A"
                
                query_c = "INSERT INTO conductores (nombre_completo, ci_num) VALUES (?, ?)"
                cursor.execute(query_c, (nombre_conductor, ci_conductor))
                conductor_id = cursor.lastrowid

                unidad_fiscal = datos.get("unidad_a_cargo", datos.get("unidad_fiscal", "DESCONOCIDA")).strip().upper()
                fecha_incautacion = datos.get("fecha_incautacion", "")
                fiscal_a_cargo = datos.get("fiscal_a_cargo", "").strip().upper() or "A DETERMINAR"
                causa_incautacion = datos.get("causa_incautacion", "").strip().upper()

                query_j = """
                    INSERT INTO datos_judiciales 
                    (vehiculo_id, conductor_id, fecha_incautacion, unidad_fiscal, fiscal_a_cargo, causa_incautacion) 
                    VALUES (?, ?, ?, ?, ?, ?)
                """
                cursor.execute(query_j, (vehiculo_id, conductor_id, fecha_incautacion, unidad_fiscal, fiscal_a_cargo, causa_incautacion))
                
                conn.commit()
                return True, f"Registro completado con éxito. ID de Acta: #{vehiculo_id}"

        except Exception as e:
            print(f"[ERROR CRÍTICO AL GUARDAR EN BD]: {e}")
            return False, f"Error al impactar los datos en el sistema: {str(e)}"