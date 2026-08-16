import asyncio
import logging

from app import AccessControlMiddleware, docs_router, base_router
from app.config import dp, bot

# Настройка логирования
logging.basicConfig(level=logging.INFO)


async def main():

    dp.register_outer_middleware(AccessControlMiddleware())  # каждый update
    dp.include_routers(docs_router)
    dp.include_routers(base_router)
    # Запуск бота в режиме polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
