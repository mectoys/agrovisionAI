from src.database.connectDB import get_connection
from mysql.connector import Error as MySqlError
from datetime import datetime
import secrets
from contextlib import  contextmanager
import bcrypt



class mo_Usuario:

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
    def get_usuarios():
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True)as cursor:
                    query="""
                            SELECT id, username, email, created_at as fecha_creacion, 
                            CASE  WHEN rol_id=1 THEN "Administrador" 
                            WHEN  rol_id=2 THEN "Lectura/Escritura" ELSE  "Lectura" END AS rol_id
                            FROM users WHERE status=1    
                            """
                    cursor.execute(query)
                    usuarios= cursor.fetchall()
                    return usuarios
        except Exception as e:
            print(f"Error en el Listado: {str(e)}")
            return False, "Error en el servidor", None

    @staticmethod
    def get_oneUser(iduser):
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True)as cursor:
                    query="""
                            SELECT id, username, full_name, email, created_at, rol_id 
                                FROM users 
                                WHERE status = 1  AND id =%s    
                            """
                    val=(iduser,)
                    cursor.execute(query,val)
                    return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener usuario: {str(e)}")
            return None

    @staticmethod
    def get_usuario(username, password):
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    # Consulta actualizada para incluir rol_id
                    query = """
                        SELECT id, username, password_hash, rol_id 
                        FROM users 
                        WHERE username = %s
                    """
                    cursor.execute(query, (username,))
                    usuario = cursor.fetchone()
                    print(query)
                    if not usuario:
                        return False, "Usuario no encontrado", None

                    if not bcrypt.checkpw(password.encode('utf-8'), usuario['password_hash'].encode('utf-8')):
                        return False, "Contraseña incorrecta", None

                    # Datos actualizados con rol_id
                    return True, "Autenticación exitosa", {
                        'id': usuario['id'],
                        'username': usuario['username'],
                        'rol_id': usuario['rol_id']  # Asegúrate de incluir esto
                    }

        except Exception as e:
            print(f"Error de autenticación: {str(e)}")
            return False, "Error en el servidor", None

    from mysql.connector import Error as MySqlError  # Si usas mysql-connector-python
    # Si usas PyMySQL: from pymysql import Error as MySqlError
    # Asegúrate de importar el error específico de tu conector

    @staticmethod
    def crear_usuario(obj_Usuario):
        conn = None
        try:
            conn = get_connection()
            hashed_pw = bcrypt.hashpw(obj_Usuario.clave.encode('utf-8'), bcrypt.gensalt())

            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (username, full_name, password_hash, email, rol_id) VALUES (%s, %s, %s, %s, %s)",
                    (obj_Usuario.username, obj_Usuario.full_name, hashed_pw.decode('utf-8'), obj_Usuario.email,
                     obj_Usuario.rol)
                )
                conn.commit()
                return {"success": True, "message": "Usuario creado"}

        except MySqlError as e:
            conn.rollback()
            # Analizar el código de error de MySQL
            error_code = e.args[0]
            error_message = e.msg if hasattr(e, 'msg') else str(e)

            if error_code == 1062:  # Código de error para entradas duplicadas
                if 'usuarios.username' in error_message:
                    return {"success": False, "error": "El nombre de usuario ya existe"}
                elif 'usuarios.email' in error_message:
                    return {"success": False, "error": "El correo electrónico ya existe"}
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
    def editar_usuario(obj_Usuario):
        conn = None
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET username=%s, email=%s, rol_id=%s WHERE id=%s",
                    (obj_Usuario.username, obj_Usuario.email, obj_Usuario.rol, obj_Usuario.id)
                )
                conn.commit()
                return {"success": True, "message": "Usuario actualizado"}

        except MySqlError as e:
            conn.rollback()
            # Analizar el código de error de MySQL
            error_code = e.args[0]
            error_message = e.msg if hasattr(e, 'msg') else str(e)

            if error_code == 1062:  # Código de error para entradas duplicadas
                if 'usuarios.username' in error_message:
                    return {"success": False, "error": "El nombre de usuario ya existe"}
                elif 'usuarios.email' in error_message:
                    return {"success": False, "error": "El correo electrónico ya existe"}
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
    def generar_token_recuperacion(email):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
                usuario = cursor.fetchone()
                if not usuario:
                    return None

                token = secrets.token_urlsafe(32)
                expiracion = datetime.now() + datetime.timedelta(hours=1)

                cursor.execute(
                    "INSERT INTO reset_tokens (usuario_id, token, expiracion) VALUES (%s, %s, %s)",
                    (usuario['id'], token, expiracion))
                conn.commit()
                return token
        except Exception as e:
            print(f"Error generando token: {str(e)}")
            return None
        finally:
            conn.close()

    # Añadir otros métodos necesarios (actualizar contraseña, asignar roles, etc.)

    @staticmethod
    def actualizar_password(usuario_id, pass_actual, pass_nueva):
        """
        Actualiza la contraseña validando la identidad del usuario.
        Retorna: (bool exito, str mensaje)
        """
        try:
            # 1. Preparar datos
            pass_actual_enc = pass_actual.encode('utf-8')

            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    # 2. Buscar usuario (Solo pedimos lo necesario: el hash)
                    cursor.execute("SELECT password_hash FROM users WHERE id = %s", (usuario_id,))
                    usuario = cursor.fetchone()

                    if not usuario:
                        return False, "Usuario no encontrado."

                    # 3. Validar identidad (Bcrypt)
                    # Nota: .encode() el hash de la DB si se guardó como string
                    hash_db = usuario['password_hash'].encode('utf-8')
                    if not bcrypt.checkpw(pass_actual_enc, hash_db):
                        return False, "La contraseña actual es incorrecta."

                    # 4. Encriptar nueva clave y ejecutar persistencia
                    nueva_hash = bcrypt.hashpw(pass_nueva.encode('utf-8'), bcrypt.gensalt())

                    cursor.execute(
                        "UPDATE users SET password_hash = %s WHERE id = %s",
                        (nueva_hash.decode('utf-8'), usuario_id)  # Guardamos como string
                    )

                    conn.commit()
                    return True, "Contraseña actualizada con éxito."

        except Exception as e:
            # Loguear el error real internamente, pero no exponerlo al usuario
            print(f"[ERROR SQL] mo_Usuario.actualizar_password: {str(e)}")
            return False, "Ocurrió un error interno en el servidor."

    @staticmethod
    def _ensure_active_sessions_table(cursor):
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS sesiones_activas (
                usuario_id INT PRIMARY KEY,
                session_token VARCHAR(128) NOT NULL,
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                ON UPDATE CURRENT_TIMESTAMP
                );            
            """
         #   """
          #  CREATE TABLE IF NOT EXISTS sesiones_activas (
        #        usuario_id INT PRIMARY KEY,
          #      session_token VARCHAR(128) NOT NULL,
         #       updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
          #          ON UPDATE CURRENT_TIMESTAMP
         #   )
          #"""
        )

    @staticmethod
    def set_active_session_token(usuario_id, session_token):
        conn = None
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                mo_Usuario._ensure_active_sessions_table(cursor)
                cursor.execute(
                    """
                    INSERT INTO sesiones_activas (usuario_id, session_token)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE
                        session_token = VALUES(session_token),
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (usuario_id, session_token),
                )
                conn.commit()
            return True
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"[ERROR SQL] mo_Usuario.set_active_session_token: {str(e)}")
            return False
        finally:
            if conn and conn.is_connected():
                conn.close()

    @staticmethod
    def get_active_session_token(usuario_id):
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cursor:
                    mo_Usuario._ensure_active_sessions_table(cursor)
                    cursor.execute(
                        "SELECT session_token FROM sesiones_activas WHERE usuario_id = %s",
                        (usuario_id,),
                    )
                    row = cursor.fetchone()
                    if not row:
                        return None
                    return row.get("session_token")
        except Exception as e:
            print(f"[ERROR SQL] mo_Usuario.get_active_session_token: {str(e)}")
            return None

    @staticmethod
    def clear_active_session_token(usuario_id, session_token=None):
        conn = None
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                mo_Usuario._ensure_active_sessions_table(cursor)
                if session_token:
                    cursor.execute(
                        "DELETE FROM sesiones_activas WHERE usuario_id = %s AND session_token = %s",
                        (usuario_id, session_token),
                    )
                else:
                    cursor.execute(
                        "DELETE FROM sesiones_activas WHERE usuario_id = %s",
                        (usuario_id,),
                    )
                conn.commit()
            return True
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"[ERROR SQL] mo_Usuario.clear_active_session_token: {str(e)}")
            return False
        finally:
            if conn and conn.is_connected():
                conn.close()
