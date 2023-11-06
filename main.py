import asyncio
import logging
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import admin_handlers,user_handlers
# Инициализируем логгер
logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(filename)s:%(lineno)d #%(levelname)-8s '
                               '[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot')
    # Загружаем конфиг в переменную config
    config:Config=load_config()
    # Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
    storage:MemoryStorage=MemoryStorage()
    # Инициализируем бот и диспетчер
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher(storage=storage)
    dp.include_router(admin_handlers.router)
    dp.include_router(user_handlers.router)




    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())