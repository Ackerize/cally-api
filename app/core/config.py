from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Cally-API"
    supabase_url: str
    supabase_key: str

    class Config:
        env_file = ".env"