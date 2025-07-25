from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_password: str
    database_username: str
    database_hostname: str
    database_name: str
    database_port: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    openai_api_key: str 

    class Config:
        env_file = ".env"

settings = Settings()