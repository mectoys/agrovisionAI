import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / "parameters.env"

if ENV_FILE.exists():
    load_dotenv(ENV_FILE)


def _get_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _get_int(name, default):
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


class AppConfig:
    APP_NAME = os.getenv("APP_NAME", "V-Control")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    PORT = int(os.getenv("FLASK_PORT", "5100"))
    DEBUG = _get_bool("FLASK_DEBUG", True)

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")
    SESSION_COOKIE_SECURE = _get_bool("SESSION_COOKIE_SECURE", False)
    SESSION_TIMEOUT_HOURS = _get_int("SESSION_TIMEOUT_HOURS", 4)
    PERMANENT_SESSION_LIFETIME = timedelta(hours=SESSION_TIMEOUT_HOURS)
    SESSION_REFRESH_EACH_REQUEST = _get_bool("SESSION_REFRESH_EACH_REQUEST", True)

    MYSQL_HOST = os.getenv("MY_SQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MY_SQL_PORT", "3306"))
    MYSQL_USER = os.getenv("MY_SQL_USER", "")
    MYSQL_PASSWORD = os.getenv("MY_SQL_PASSWORD", "")
    MYSQL_DATABASE = os.getenv("MY_SQL_DATABASE", "")
    MYSQL_POOL_NAME = os.getenv("MY_SQL_POOL_NAME", "mypool")
    MYSQL_POOL_SIZE = int(os.getenv("MY_SQL_POOL_SIZE", "5"))
    MYSQL_SSL_DISABLED = _get_bool("MY_SQL_SSL_DISABLED", False)
    MYSQL_SSL_CA = os.getenv("MY_SQL_SSL_CA", "")
    MYSQL_SSL_CERT = os.getenv("MY_SQL_SSL_CERT", "")
    MYSQL_SSL_KEY = os.getenv("MY_SQL_SSL_KEY", "")
    MYSQL_SSL_VERIFY_CERT = _get_bool("MY_SQL_SSL_VERIFY_CERT", False)
    MYSQL_SSL_VERIFY_IDENTITY = _get_bool("MY_SQL_SSL_VERIFY_IDENTITY", False)
    MYSQL_TLS_VERSIONS = [
        version.strip()
        for version in os.getenv("MY_SQL_TLS_VERSIONS", "TLSv1.2,TLSv1.3").split(",")
        if version.strip()
    ]

    APIS_PERU_TOKEN = os.getenv("APIS_PERU_TOKEN", "")
    APIS_PERU_URL = os.getenv("APIS_PERU_URL", "http://api.decolecta.com")

    TESSERACT_CMD = os.getenv("TESSERACT_CMD", r"C:\Program Files\Tesseract-OCR\tesseract.exe")
    OCR_INPUT_DIR = os.getenv(
        "OCR_INPUT_DIR",
        r"D:\Proyectos\Trabajo Empresas\ARDICORP\Guia Remision sello agencia\scaneados",
    )
