import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Wireworld Simulator API"
    CHALLENGE_FILE: str = "challenge.toml"
    FLAG: str = os.environ.get("GZCTF_FLAG", "flag{test_flag}")

    class Config:
        env_file = ".env"


settings = Settings()
