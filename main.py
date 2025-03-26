from aiogram import Bot, Dispatcher
import asyncio
from config import TOKEN, logger, my_commands
from app.handlers import router
from app.database.models import async_main


async def main():
    if not TOKEN:
        raise ValueError("You must provide a token before creating a new instance of the bot.")
    await async_main()
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router=router)
    await bot.delete_my_commands()
    await bot.set_my_commands(commands=my_commands)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        logger.info('Bot started.')
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Bot stopped.')
        exit(1)
