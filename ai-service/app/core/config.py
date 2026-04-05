from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AI_", env_file=".env", extra="ignore")

    llm_name: str = "gpt-4o-mini"
    minimum_keyword_count: int = 15


settings = Settings()
