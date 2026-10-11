from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    app_name: str = "Talko Backend"
    gemini_api_key: str
    gemini_model: str = "gemini-3.6-flash"
    database_url: str = "sqlite:///./talko.db"

    supabase_url: str = ""
    supabase_publishable_key: str = ""
    supabase_secret_key: str = ""
    supabase_jwks_url: str = ""


settings = Settings()
