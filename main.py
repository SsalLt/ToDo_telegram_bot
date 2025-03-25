from aiogram import Bot, Dispatcher
import asyncio
from config import TOKEN, logger, my_commands
from app.handlers import router
from app.database.models import async_main
import logging


async def main():
    await async_main()  # Initialize database connection
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router=router)
    await bot.delete_my_commands()
    await bot.set_my_commands(commands=my_commands)
    await dp.start_polling(bot)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    try:
        logger.info('Bot started.')
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Bot stopped.')
        exit(1)
