from os import environ, path
from dotenv import load_dotenv


dotenv_path = path.join(path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)


class DefaultSettings:
    """
    Default config for application.
    """
    BOT_TOKEN: str = environ.get("BOT_TOKEN", "")
    ADMIN_ID: str = environ.get("ADMIN_ID", "")

    POSTGRES_DB: str = environ.get("POSTGRES_DB", "timetable_db")
    POSTGRES_HOST: str = environ.get("POSTGRES_HOST", "localhost")
    POSTGRES_USER: str = environ.get("POSTGRES_USER", "user")
    POSTGRES_PORT: int = int(environ.get("POSTGRES_PORT", "5432")[-4:])
    POSTGRES_PASSWORD: str = environ.get("POSTGRES_PASSWORD", "funnypassword")
    # DB_CONNECT_RETRY: int = environ.get("DB_CONNECT_RETRY", 20)
    # DB_POOL_SIZE: int = environ.get("DB_POOL_SIZE", 15)

    TIMEZONE_OFFSET: int = 3
    NEW_SEMESTER_STARTS: str = "2023-02-05"
    FILE_FOR_PDF_FILE_ID: str = "pdffileid"

    @property
    def database_settings(self) -> dict:
        """
        Get all settings for connection with database.
        """
        return {
            "database": self.POSTGRES_DB,
            "user": self.POSTGRES_USER,
            "password": self.POSTGRES_PASSWORD,
            "host": self.POSTGRES_HOST,
            "port": self.POSTGRES_PORT,
        }

    @property
    def database_uri(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    @property
    def database_uri_sync(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
