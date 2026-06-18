from src.database.connectDB import get_connection
from mysql.connector import Error as MySqlError
from datetime import datetime
import secrets
from contextlib import contextmanager



class plot_model:

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
    def get_plots(companyid):
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    query = """
                            SELECT id, farm_id,crop_id,name, planted_date,area 
                            FROM plots
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
    def get_oneplot(idplot, companyid):
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    query = """
                            SELECT id, farm_id, crop_id, name, planted_date, area 
                            FROM plots
                            WHERE id = %s  AND company_id= %s
                            """
                    val = (idplot, companyid)
                    cursor.execute(query, val)
                    return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener Cultivos: {str(e)}")
            return None

    @staticmethod
    def save_plot(obj_plot):
        conn = None
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO plots (farm_id, crop_id, name, planted_date, area , company_id)"
                    " VALUES (%s, %s, %s,  %s, %s,  %s)",
                    (obj_plot.farm_id, obj_plot.crop_id, obj_plot.name, obj_plot.planted_date, obj_plot.area,
                     obj_plot.company_id)
                )
                conn.commit()
                return {"success": True, "message": "Parcela creado"}

        except MySqlError as e:
            conn.rollback()
            # Analizar el código de error de MySQL
            error_code = e.args[0]
            error_message = e.msg if hasattr(e, 'msg') else str(e)

            if error_code == 1062:  # Código de error para entradas duplicadas
                if 'plots.name' in error_message:
                    return {"success": False, "error": "El nombre de Cultivo ya existe"}

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
    def update_plot(obj_plot):
        conn = None
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    """                    
                    UPDATE plots
                    SET farm_id = %s,
                        crop_id = %s,
                        name    =   %s,
                        planted_date = %s,
                        area = %s,
                    WHERE id = %s AND company_id = %s
                    """,
                    (obj_plot.farm_id , obj_plot.crop_id, obj_plot.name, obj_plot.planted_date, obj_plot.area,
                     obj_plot.crop_id, obj_plot.company_id)
                )
                conn.commit()
                return {"success": True, "message": "Parcela actualizado"}

        except MySqlError as e:
            conn.rollback()
            error_code = e.args[0]
            error_message = e.msg if hasattr(e, 'msg') else str(e)

            if error_code == 1062:
                if 'plots.name' in error_message:
                    return {"success": False, "error": "El nombre de Parcela ya existe"}
                else:
                    return {"success": False, "error": "Dato duplicado en la base de datos"}
            return {"success": False, "error": f"Error de base de datos: {error_message}"}

        except Exception as e:
            conn.rollback()
            return {"success": False, "error": f"Error inesperado: {str(e)}"}

        finally:
            if conn and conn.is_connected():
                conn.close()
