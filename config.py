import os
from urllib.parse import quote_plus

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def _env_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class Config:

    PRODUCTION = _env_bool("FLASK_PRODUCTION", _env_bool("RENDER"))
    DEBUG = _env_bool("FLASK_DEBUG")
    TESTING = False

    _secret_key = os.getenv("SECRET_KEY", "").strip()
    if PRODUCTION and not _secret_key:
        raise RuntimeError("Definir SECRET_KEY como variable de entorno en producción.")
    SECRET_KEY = _secret_key or "clave-desarrollo-cambiar"

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "portfolio_db")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{quote_plus(DB_USER)}:{quote_plus(DB_PASSWORD)}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    )

    _connect_args = {"connect_timeout": 10}
    _ssl_ca = os.getenv("DB_SSL_CA", "").strip()
    if _ssl_ca:
        _connect_args["ssl_ca"] = _ssl_ca
        _connect_args["ssl_verify_cert"] = True
        _connect_args["ssl_verify_identity"] = _env_bool("DB_SSL_VERIFY_IDENTITY", True)

    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": _connect_args,
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_size": int(os.getenv("DB_POOL_SIZE", "5")),
        "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "2")),
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False
