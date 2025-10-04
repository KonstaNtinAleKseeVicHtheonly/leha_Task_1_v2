from dataclasses import dataclass
from decouple import config


@dataclass
class DataBaseModel:
    host: str = config("HOST")
    port: str = config("PORT")
    DB_name: str = config("DB_NAME")
    login: str = config("LOGIN")
    password: str = config("PASSWORD")

    def __post_init__(self):
        self.DB_URL: str = f"postgresql+asyncpg://{self.login}:{self.password}@{self.host}:{self.port}/{self.DB_name}"
