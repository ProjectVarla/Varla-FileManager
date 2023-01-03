from ipaddress import IPv4Address
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseSettings, validator

load_dotenv()


class Settings(BaseSettings):

    APP_NAME: str = "File-Manager"
    APP_TYPE: str = "Service"

    GATEWAY_URL: str

    FILE_MANAGER_PORT: int
    FILE_MANAGER_HOST: str
    BACKUP_CONFIG_PATH: str
    BACKUP_TEMPORARY_PATH: str

    DEBUG_MODE: Optional[bool] = False
    NOTIFICATION_CORE_URL: Optional[str]
    DEFAULT_CHANNEL: Optional[str]

    @validator("FILE_MANAGER_HOST", always=True)
    def file_manager_host_validator(cls, v):
        return str(IPv4Address(v))

    @validator("NOTIFICATION_CORE_URL", always=True)
    def notification_core_url_validator(cls, v, values):
        return values["GATEWAY_URL"]


settings = Settings()
