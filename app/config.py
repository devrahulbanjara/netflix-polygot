from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # PostgreSQL
    PG_HOST: str = "localhost"
    PG_PORT: int = 5432
    PG_USER: str = "netflix"
    PG_PASSWORD: str = "secret123"
    PG_DB: str = "netflix_users"

    # MongoDB
    MONGO_HOST: str = "localhost"
    MONGO_PORT: int = 27017
    MONGO_USER: str = "netflix"
    MONGO_PASSWORD: str = "secret123"
    MONGO_DB: str = "netflix_catalog"

    @property
    def pg_dsn(self) -> str:
        return (
            f"postgresql://{self.PG_USER}:{self.PG_PASSWORD}"
            f"@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"
        )

    @property
    def mongo_uri(self) -> str:
        return (
            f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}"
            f"@{self.MONGO_HOST}:{self.MONGO_PORT}"
        )

settings = Settings()