from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    server: str
    database: str
    username: str
    password: str = ""
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file =".env"




settings = Settings()