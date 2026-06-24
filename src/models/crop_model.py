from src.database.connectDB import get_connection
from mysql.connector import Error as MySqlError
from datetime import datetime
import secrets
from contextlib import contextmanager



class crop_model:

    @staticmethod
    @contextmanager
    def get_managed_connection():
        connection = get_connection()
        try:
            yield connection
        finally:
            if connection:
                connection.close()

    @staticmethod
    def get_crops(companyid):
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    query = """
                            SELECT id, name as descripcion, scientific_name, description, created_at as fecha_creacion
                            FROM crops  
                            WHERE company_id  =%s
                            """
                    val = (companyid,)
                    cursor.execute(query, val)
                    crops = cursor.fetchall()
                    return crops
        except Exception as e:
            print(f"Error en el Listado: {str(e)}")
            return False, "Error en el servidor", None

    @staticmethod
    def get_onecrop(idcrop, companyid):
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    query = """
                            SELECT id, name, scientific_name, description, created_at as fecha_creacion
                            FROM crops 
                            WHERE id = %s  AND company_id= %s
                            """
                    val = (idcrop, companyid)
                    cursor.execute(query, val)
                    return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener Cultivos: {str(e)}")
            return None

    @staticmethod
    def save_farm(obj_crop):
        conn = None
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO crops (name, scientific_name, description, company_id)"
                    " VALUES (%s, %s, %s,  %s)",
                    (obj_crop.name, obj_crop.scientific_name, obj_crop.description, obj_crop.company_id)
                )
                conn.commit()
                return {"success": True, "message": "Cultivo creado"}

        except MySqlError as e:
            conn.rollback()
            # Analizar el código de error de MySQL
            error_code = e.args[0]
            error_message = e.msg if hasattr(e, 'msg') else str(e)

            if error_code == 1062:  # Código de error para entradas duplicadas
                if 'crops.name' in error_message:
                    return {"success": False, "error": "El nombre de Cultivo ya existe"}
                elif 'crops.scientific_name' in error_message:
                    return {"success": False, "error": "El nombre Científico ya existe"}
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
    def update_crop(obj_crop):
        conn = None
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE crops
                    SET name = %s,
                        scientific_name = %s,
                        description = %s
                    WHERE id = %s AND company_id = %s
                    """,
                    (obj_crop.name, obj_crop.scientific_name, obj_crop.description, obj_crop.id, obj_crop.company_id)
                )
                conn.commit()
                return {"success": True, "message": "Cultivo actualizado"}

        except MySqlError as e:
            conn.rollback()
            error_code = e.args[0]
            error_message = e.msg if hasattr(e, 'msg') else str(e)

            if error_code == 1062:
                if 'crops.name' in error_message:
                    return {"success": False, "error": "El nombre de Cultivo ya existe"}
                elif 'crops.scientific_name' in error_message:
                    return {"success": False, "error": "El nombre Científico ya existe"}
                else:
                    return {"success": False, "error": "Dato duplicado en la base de datos"}
            return {"success": False, "error": f"Error de base de datos: {error_message}"}

        except Exception as e:
            conn.rollback()
            return {"success": False, "error": f"Error inesperado: {str(e)}"}

        finally:
            if conn and conn.is_connected():
                conn.close()
