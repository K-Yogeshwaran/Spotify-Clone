from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Spotify Clone API"
    database_url: str = "sqlite:///./spotify_clone.db"
    supabase_url: str = ""
    supabase_key: str = ""
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 120
    jwt_algorithm: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
