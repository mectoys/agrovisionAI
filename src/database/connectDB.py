import logging

from mysql.connector.pooling import Error, MySQLConnectionPool

from config import AppConfig


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


if not all([
    AppConfig.MYSQL_HOST,
    AppConfig.MYSQL_USER,
    AppConfig.MYSQL_PASSWORD,
    AppConfig.MYSQL_DATABASE,
]):
    logger.critical("Faltan variables de entorno necesarias para la conexión a la base de datos.")
    raise Exception("Faltan variables de entorno necesarias.")


def _build_connection_config():
    connection_config = {
        "pool_name": AppConfig.MYSQL_POOL_NAME,
        "pool_size": AppConfig.MYSQL_POOL_SIZE,
        "pool_reset_session": True,
        "host": AppConfig.MYSQL_HOST,
        "port": AppConfig.MYSQL_PORT,
        "user": AppConfig.MYSQL_USER,
        "password": AppConfig.MYSQL_PASSWORD,
        "database": AppConfig.MYSQL_DATABASE,
        "ssl_disabled": AppConfig.MYSQL_SSL_DISABLED,
    }

    if AppConfig.MYSQL_TLS_VERSIONS:
        connection_config["tls_versions"] = AppConfig.MYSQL_TLS_VERSIONS

    if AppConfig.MYSQL_SSL_CA:
        connection_config["ssl_ca"] = AppConfig.MYSQL_SSL_CA
        connection_config["ssl_verify_cert"] = AppConfig.MYSQL_SSL_VERIFY_CERT
        connection_config["ssl_verify_identity"] = AppConfig.MYSQL_SSL_VERIFY_IDENTITY

    if AppConfig.MYSQL_SSL_CERT:
        connection_config["ssl_cert"] = AppConfig.MYSQL_SSL_CERT

    if AppConfig.MYSQL_SSL_KEY:
        connection_config["ssl_key"] = AppConfig.MYSQL_SSL_KEY

    return connection_config


try:
    connection_pool = MySQLConnectionPool(**_build_connection_config())
    logger.info(
        "Pool de conexiones configurado correctamente para %s:%s/%s.",
        AppConfig.MYSQL_HOST,
        AppConfig.MYSQL_PORT,
        AppConfig.MYSQL_DATABASE,
    )
except Error as err:
    logger.critical(f"Error al configurar el pool de conexiones: {err}")
    raise err


def get_connection():
    try:
        return connection_pool.get_connection()
    except Error as err:
        if err.errno == 1045:
            logger.error("Error de autenticación con la base de datos.")
        elif err.errno == 2003:
            logger.error("No se puede conectar a la base de datos.")
        elif err.errno == 2026:
            logger.error(
                "Error SSL/TLS al conectarse a MySQL. Revisa el puerto, el CA certificado y los parámetros TLS."
            )
        else:
            logger.error(f"Error desconocido: {err}")
        raise err
