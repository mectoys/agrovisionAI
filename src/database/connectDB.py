from config import AppConfig
import logging
from mysql.connector.pooling import MySQLConnectionPool, Error

# Configuración del logging
logging.basicConfig(
    level=logging.INFO,  # Nivel de los mensajes de log que se mostrarán (INFO o superior).
    format='%(asctime)s - %(levelname)s - %(message)s',  # Define el formato de los mensajes de log.
    handlers=[
        logging.FileHandler("app.log"),  # Guarda los mensajes de log en un archivo llamado "app.log".
        logging.StreamHandler()  # También muestra los mensajes en la consola.
    ]
)

# Crea un logger para la aplicación, que se utilizará para escribir mensajes de log en diferentes niveles.
logger = logging.getLogger(__name__)

# Verifica que todas las variables de entorno necesarias para conectarse a la base de datos estén definidas.
if not all([AppConfig.MYSQL_HOST, AppConfig.MYSQL_USER, AppConfig.MYSQL_PASSWORD,
            AppConfig.MYSQL_DATABASE]):
    # Si falta alguna variable, se genera un mensaje crítico en el log y se lanza una excepción.
    logger.critical("Faltan variables de entorno necesarias para la conexión a la base de datos.")
    raise Exception("Faltan variables de entorno necesarias.")

# Configurar el pool de conexiones
# Intenta crear un pool de conexiones a MySQL con los parámetros especificados.
try:
    connection_pool = MySQLConnectionPool(
        pool_name=AppConfig.MYSQL_POOL_NAME,  # Nombre asignado al pool de conexiones.
        pool_size=AppConfig.MYSQL_POOL_SIZE,  # Tamaño máximo del pool de conexiones.
        pool_reset_session=True,  # Restablece el estado de la conexión antes de que se reutilice.
        host=AppConfig.MYSQL_HOST,  # Host de la base de datos MySQL, obtenido del archivo .env.
        user=AppConfig.MYSQL_USER,  # Usuario de la base de datos.
        password=AppConfig.MYSQL_PASSWORD,  # Contraseña de la base de datos.
        database=AppConfig.MYSQL_DATABASE  # Nombre de la base de datos a la que se conecta.

    )

    # Si la configuración es exitosa, se genera un mensaje informativo en el log.
    logger.info("Pool de conexiones configurado correctamente.")
except Error as err:
    # Si ocurre un error durante la configuración del pool, se registra el error y se lanza una excepción.
    logger.critical(f"Error al configurar el pool de conexiones: {err}")
    raise err


# Función para obtener una conexión del pool
def get_connection():
    try:
        return connection_pool.get_connection()
    except Error as err:
        # Maneja posibles errores al obtener la conexión.
        if err.errno == 1045:  # Error de autenticación.
            logger.error("Error de autenticación con la base de datos.")
        elif err.errno == 2003:  # Error al conectarse al servidor MySQL.
            logger.error("No se puede conectar a la base de datos.")
        else:
            # Cualquier otro error se registra en el log.
            logger.error(f"Error desconocido: {err}")
        # Lanza de nuevo el error para manejarlo en otro lugar si es necesario.
        raise err
