from __future__ import annotations

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class BotConfig(BaseSettings):
    """Bot configuration"""

    token: str
    parse_mode: str


class DBConfig(BaseSettings):
    """Database configuration"""

    postgres_dsn: str
    redis_host: str
    redis_port: int
    redis_db: int


class Config(BaseSettings):
    """Main configuration"""

    bot_config: BotConfig
    db_config: DBConfig
    admins: list[int]
    i18n_format_key: str
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str


    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    ) # type: ignore


config = Config() # type: ignore

