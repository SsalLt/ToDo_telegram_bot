from aiogram.types import BotCommand
from dotenv import load_dotenv
import logging
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')

my_commands: list[BotCommand] = [
    BotCommand(command="start", description="▶ Запустить бота"),
    BotCommand(command="add", description="🆕 Добавить новую задачу"),
    BotCommand(command="my_tasks", description="📋 Список задач"),
    BotCommand(command="delete", description="🗑 Удалить выполненные задачи")
]


def _get_logger() -> logging.Logger:
    logging.getLogger().setLevel(logging.CRITICAL)
    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.DEBUG)
    _formatter = logging.Formatter(fmt='%(asctime)s - %(filename)s - %(levelname)s - %(message)s',
                                   datefmt='%d.%m.%Y (%H:%M:%S)')
    _console_handler = logging.StreamHandler()
    _console_handler.setLevel(logging.DEBUG)
    _console_handler.setFormatter(_formatter)
    _logger.addHandler(_console_handler)
    return _logger


logger = _get_logger()
del _get_logger

__all__ = ['TOKEN', 'logger', 'my_commands']
