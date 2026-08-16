import asyncio
import logging

from app import AccessControlMiddleware, docs_router, base_router
from app.config import dp, bot
from config import settings
from pipline import run_pipline

# Настройка логирования
logging.basicConfig(level=logging.INFO)


async def hourly_task():
    while True:
        try:
            await run_pipline()
        except Exception as e:
            await bot.send_message(
                user_id=int(settings.TECH_ADMIN),
                text=f"Произошла ошибка при загрузке данных {e}",
            )
            print(f"Ошибка: {e}")

        await asyncio.sleep(3600)


async def main():
    asyncio.create_task(hourly_task())

    dp.register_outer_middleware(AccessControlMiddleware())  # каждый update
    dp.include_routers(docs_router)
    dp.include_routers(base_router)
    # Запуск бота в режиме polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
