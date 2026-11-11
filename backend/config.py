import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))
load_dotenv()


def _normalize_database_url(url: str) -> str:
    """Cloud plugins (Railway, PlanetScale, ...) hand out bare mysql:// URLs;
    SQLAlchemy needs the driver spelled out."""
    if url.startswith("mysql://"):
        return "mysql+pymysql://" + url[len("mysql://"):]
    if url.startswith("postgres://"):
        return "postgresql://" + url[len("postgres://"):]
    return url


DATABASE_URL = _normalize_database_url(os.getenv("DATABASE_URL")) if os.getenv("DATABASE_URL") else None


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