import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from app.bot.routers.link import router as link_router

from app.core.settings.config import Settings, get_settings

settings: Settings = get_settings()

dp = Dispatcher()


async def main() -> None:
    logging.info("Starting server...")
    logging.info(f"Token: {settings.BOT_TOKEN}")
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp.include_router(link_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
