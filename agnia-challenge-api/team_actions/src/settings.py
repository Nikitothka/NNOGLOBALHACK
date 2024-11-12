import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    team_id: str = "b98cc43e-09c6-4c47-a0c0-947e8701879f"
    backend_api: str = "https://aes-agniachallenge-case.olymp.innopolis.university/"
    root_directory: str = os.path.dirname(__file__)
    integration_api: str = "https://aiteamtg.store/api"


settings = Settings()
