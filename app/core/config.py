from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """โหลดค่า config จากไฟล์ .env"""
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    app_name: str = "Talko Backend"
    gemini_api_key: str                       # ต้องมีใน .env
    gemini_model: str = "gemini-3.6-flash"    # เปลี่ยนได้ถ้า AI Studio มีรุ่นอื่น


settings = Settings()
