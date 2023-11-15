from aiogram import Bot, Dispatcher
from pydantic import SecretStr, PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TOKEN: SecretStr
    DATABASE_URL: PostgresDsn


settings = Settings()
bot = Bot(
    token=settings.TOKEN.get_secret_value(),
    parse_mode="HTML"
)
dp = Dispatcher()
