from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    host_system: str
    port_system: int
    log_level: str
    access_log: bool

    class Config:
        env_file = ".env"
