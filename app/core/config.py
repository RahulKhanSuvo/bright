from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    secret_key: str = Field(validation_alias="SECRET_KEY")
    algorithm: str = Field(
        default="HS256",
        validation_alias="ALGORITHM",
    )
    access_token_expire_minutes: int = Field(
        default=30,
        validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES",
    )
    database_url: str = Field(validation_alias="DATABASE_URL")
    cookie_secure: bool = Field(default=False, validation_alias="COOKIE_SECURE")


settings = Settings()  # pyright: ignore[reportCallIssue]
