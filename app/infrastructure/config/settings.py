from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    soap_base_url: str
    soap_timeout: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="SOAP_",
        extra="ignore",
    )
