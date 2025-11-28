from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Sistema Educativo API"
    SECRET_KEY: str = "CHANGE_ME"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    CORS_ORIGINS: str = "http://localhost:5173"
    DATABASE_URL: str = "mysql://user:password@localhost:3306/sistema_edu"

    class Config:
        env_file = ".env"

settings = Settings()
