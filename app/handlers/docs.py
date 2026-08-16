from maxapi import Router
from maxapi.types import MessageCreated, Command, InputMedia
from doc_utils import get_archive
from app.config import bot

router = Router(router_id="docs_router")


# # Обработчик всех текстовых сообщений
# @dp.message_created()
# async def echo_handler(event: MessageCreated):
#     if event.message.body.text:

#         # 2. Собираем финальный текст через официальный as_markdown
#         text = as_markdown(
#             Heading("📊 Отчёт по компонентам системы"),
#             "\n",
#             Bold("Данные актуальны на текущий час:"),
#         )

#         # 3. Отправляем в чат с правильным Enum-форматом
#         await event.message.answer(text, format=Format.MARKDOWN)


@router.message_created(Command("get_all_docs_dummy"))
async def dummy_handler(event: MessageCreated):
    await event.message.answer("Произошла ошибка при формировании документа")


@router.message_created(Command("get_all_docs"))
async def docs_handler(event: MessageCreated):
    path2_docs = "data/students_data"
    output_path = "data/archives/student_docs"
    res = get_archive(path2_docs, output_path, rewrite=True)

    if res:
        await event.message.answer("Заполненные документы по всем пользователям:")
        await bot.send_message(
            chat_id=event.message.recipient.chat_id,
            attachments=[
                InputMedia(path=output_path + ".zip"),
            ],
        )
    else:
        await event.message.answer("Произошла ошибка при формировании документа")
