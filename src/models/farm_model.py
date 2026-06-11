from src.database.connectDB import get_connection
from mysql.connector import Error as MySqlError
from datetime import datetime
import secrets
from contextlib import  contextmanager
import bcrypt

class farm_model:

    @staticmethod
    @contextmanager
    def get_managed_connection():
        connection =get_connection()
        try:
            yield  connection
        finally:
            if connection:
                connection.close()

    @staticmethod
    def get_farms():
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True)as cursor:
                    query="""
                            SELECT id, name, location, area_hectares, created_at as fecha_creacion
                            FROM farms    
                            """
                    cursor.execute(query)
                    usuarios= cursor.fetchall()
                    return usuarios
        except Exception as e:
            print(f"Error en el Listado: {str(e)}")
            return False, "Error en el servidor", None


    @staticmethod
    def get_onefarm(idfarm):
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True)as cursor:
                    query="""
                            SELECT id,name,location,area_hectares,created_at 
                            FROM farms 
                            WHERE id = %s    
                            """
                    val=(idfarm,)
                    cursor.execute(query,val)
                    return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener Fundo: {str(e)}")
            return None

    @staticmethod
    def save_farm(obj_farm):
        conn = None
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO farms (name, user_id, location, area_hectares) VALUES (%s, %s, %s, %s)",
                    (obj_farm.name, obj_farm.user_id, obj_farm.location, obj_farm.area_hectares)
                )
                conn.commit()
                return {"success": True, "message": "Fundo creado"}

        except MySqlError as e:
            conn.rollback()
            # Analizar el código de error de MySQL
            error_code = e.args[0]
            error_message = e.msg if hasattr(e, 'msg') else str(e)

            if error_code == 1062:  # Código de error para entradas duplicadas
                if 'farms.name' in error_message:
                    return {"success": False, "error": "El nombre de Fundo ya existe"}
                elif 'farms.location' in error_message:
                    return {"success": False, "error": "La Ubicación ya existe"}
                else:
                    return {"success": False, "error": "Dato duplicado en la base de datos"}
            else:
                return {"success": False, "error": f"Error de base de datos: {error_message}"}

        except Exception as e:
            conn.rollback()
            return {"success": False, "error": f"Error inesperado: {str(e)}"}

        finally:
            if conn and conn.is_connected():
                conn.close()

    @staticmethod
    def update_farm(obj_farm):
        conn = None
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE farms
                    SET name = %s,
                        location = %s,
                        area_hectares = %s
                    WHERE id = %s
                    """,
                    (obj_farm.name, obj_farm.location, obj_farm.area_hectares, obj_farm.id)
                )
                conn.commit()
                return {"success": True, "message": "Fundo actualizado"}

        except MySqlError as e:
            conn.rollback()
            error_code = e.args[0]
            error_message = e.msg if hasattr(e, 'msg') else str(e)

            if error_code == 1062:
                if 'farms.name' in error_message:
                    return {"success": False, "error": "El nombre de Fundo ya existe"}
                elif 'farms.location' in error_message:
                    return {"success": False, "error": "La Ubicación ya existe"}
                else:
                    return {"success": False, "error": "Dato duplicado en la base de datos"}
            return {"success": False, "error": f"Error de base de datos: {error_message}"}

        except Exception as e:
            conn.rollback()
            return {"success": False, "error": f"Error inesperado: {str(e)}"}

        finally:
            if conn and conn.is_connected():
                conn.close()
