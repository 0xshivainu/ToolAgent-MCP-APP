from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_key: str
    base_url: str

    class Config:
        env_file = ".env"  # 指定從 .env 讀取設定


settings = Settings()