import os
from urllib.parse import parse_qsl, urlencode

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))
load_dotenv()


def _process_mysql_url(url: str) -> tuple:
    """Cloud MySQL plugins hand out libmysqlclient-style URLs
    (mysql://...?ssl-mode=REQUIRED). SQLAlchemy needs the driver spelled out,
    and pymysql rejects libmysql-only kwargs like 'ssl-mode'.
    Returns (cleaned_url, connect_args dict with real booleans)."""
    connect_args = {}
    if url.startswith("mysql://"):
        url = "mysql+pymysql://" + url[len("mysql://"):]
    elif url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]

    if "?" in url:
        base, query = url.split("?", 1)
        params = parse_qsl(query, keep_blank_values=True)
        kept = []
        ssl_mode = None
        for k, v in params:
            kl = k.lower()
            if kl == "ssl-mode":
                ssl_mode = v.lower()
            elif kl == "ssl-ca":
                connect_args["ssl_ca"] = v
            elif kl == "ssl-cert":
                connect_args["ssl_cert"] = v
            elif kl == "ssl-key":
                connect_args["ssl_key"] = v
            elif kl == "ssl-key-password":
                connect_args["ssl_key_password"] = v
            else:
                kept.append((k, v))

        if ssl_mode:
            if ssl_mode == "disabled":
                connect_args["ssl_disabled"] = True
            elif ssl_mode == "required":
                connect_args["ssl_required"] = True
            elif ssl_mode == "verify_ca":
                connect_args["ssl_required"] = True
                connect_args["ssl_verify_cert"] = True
            elif ssl_mode == "verify_identity":
                connect_args["ssl_required"] = True
                connect_args["ssl_verify_cert"] = True
                connect_args["ssl_verify_identity"] = True

        url = base + ("?" + urlencode(kept) if kept else "")

    return url, connect_args


if os.getenv("DATABASE_URL"):
    DATABASE_URL, _CONNECT_ARGS = _process_mysql_url(os.getenv("DATABASE_URL"))
else:
    DATABASE_URL, _CONNECT_ARGS = None, {}


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "project_db")

    SQLALCHEMY_DATABASE_URI = (
        DATABASE_URL
        or f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    SQLALCHEMY_ENGINE_OPTIONS = {"connect_args": _CONNECT_ARGS} if _CONNECT_ARGS else {}

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY"
    )


    OPENAI_API_KEY = os.getenv(
        "OPENAI_API_KEY"
    )


    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY"
    )


    LLM_PROVIDER = os.getenv(
        "LLM_PROVIDER"
    )
