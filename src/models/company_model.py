from src.database.connectDB import get_connection
from mysql.connector import Error as MySqlError

from contextlib import contextmanager

class company_model:

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
    def get_by_ruc(ruc):
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    query = """
                            SELECT *
                            FROM companies  
                            WHERE ruc  =%s
                            """
                    val = (ruc,)
                    cursor.execute(query, val)
                    companies = cursor.fetchone()
                    return companies
        except Exception as e:
            print(f"Error en la lista: {str(e)}")
            return False, "Error en el servidor", None
