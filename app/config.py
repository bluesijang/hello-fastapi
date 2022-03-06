from pydantic import BaseSettings

# variable type = <default>
# 환경변수를 활용하는 방법
class Settings(BaseSettings):
    database_hostname: str
    database_port: str    
    database_password: str
    database_name: str
    database_username: str    
    secrete_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()
