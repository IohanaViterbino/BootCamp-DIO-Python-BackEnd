# arquivo onde cria as configurações da api personalizada

from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL: str = Field(default='mysql+aiomysql://root:my123SQL@localhost/workout')


settings = Settings()