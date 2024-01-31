from pydantic_settings import BaseSettings
from pydantic import ConfigDict, field_validator, EmailStr


class Settings(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://postgres:567234@localhost:5432/abc"
    SECRET_KEY_JWT: str = "1234567890"

    ALGORITHM: str = "HS256"
    MAIL_USERNAME: str = "example@gmail.com"
    MAIL_PASSWORD: str = "postgres"
    MAIL_FROM: str = "potgres@gmail.com"
    MAIL_PORT: int = 6379
    MAIL_SERVER: str = "postgres"

    REDIS_DOMAIN: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""

    CLOUDINARY_NAME: str = "abc"
    CLOUDINARY_API_KEY: int = 000000000000000
    CLOUDINARY_API_SECRET: str = "secret"

    model_config = ConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8"
    )

    @field_validator("ALGORITHM")
    @classmethod
    def validate_algorithm(cls, value):
        if value not in ["HS256", "HS512"]:
            raise ValueError("Algorithm must be HS256 or HS512")

        return value


config = Settings()