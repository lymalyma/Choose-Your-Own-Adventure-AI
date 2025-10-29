from typing import List 
from pydantic_settings import BaseSettings, SettingsConfigDict  # <-- Import this
from pydantic import field_validator

class Settings(BaseSettings): 
    # 1. Define the config *inside* the class using 'model_config'
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

    # 2. Now define your fields
    API_PREFIX: str = '/api'
    DEBUG: bool = False 
    DATABASE_URL: str 
    ALLOWED_ORIGINS: str = ""
    OPENAI_API_KEY: str

    """
    We need this because the env files files do not support a list, 
    we have to parse it and return a list. We have entered it as a items separated by commas
    """
    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v: str) -> List[str]: 
        return v.split(",") if v else []

# 3. You no longer need this separate Config class
# class Config: 
#     env_file = ".env"
#     env_file_encoding = "utf-8"
#     case_sensitive = True

# 4. This line will now work!
settings = Settings()