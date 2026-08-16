from yandex_form.model import FormLoader
from doc_utils.personal_card import PersonalCard
from doc_utils.data_process import process_form_data
from google_sheet.models import ToSheetFormater
from config import settings


import asyncio
import logging

from app import AccessControlMiddleware, docs_router, base_router
from app.config import dp, bot

# Настройка логирования
logging.basicConfig(level=logging.INFO)


# def main():
#     form = FormLoader()
#     google_formater = ToSheetFormater()
#     personal_card = PersonalCard()

#     # if settings.SURVEY_ID:
#     #     # загружаем данные
#     #     form.load_data(settings.SURVEY_ID, output_path="data/yandex_form.csv")

#     # Приводим в порядок таблицу с студентами
#     students = process_form_data("data/yandex_form.csv")
#     # Заполняем документ
#     personal_card.complit(students)
#     # загружаем на гугл таблицу
#     google_formater.add(students)


async def main():

    dp.register_outer_middleware(AccessControlMiddleware())  # каждый update
    dp.include_routers(docs_router)
    dp.include_routers(base_router)
    # Запуск бота в режиме polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
