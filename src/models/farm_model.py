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
                            WHERE id=id =%s    
                            """
                    val=(idfarm,)
                    cursor.execute(query,val)
                    return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener Fundo: {str(e)}")
            return None