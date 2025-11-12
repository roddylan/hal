from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    cloudflare_account_id: str
    cloudflare_api_token: str

    gemini_api_token: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
