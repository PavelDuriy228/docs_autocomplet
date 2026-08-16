from maxapi import Router, F
from maxapi.types import MessageCreated, Command, InputMedia
from doc_utils import get_archive
from app.config import bot

router = Router(router_id="docs_router")
path2_docs = "data/students_data"
output_path = "data/archives/student_docs"


@router.message_created(Command("get_all_docs"))
async def docs_handler(event: MessageCreated):
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


@router.message_created(F.message.body.text == "Получить архив документов")
async def docs_handler_keyboard(event: MessageCreated):
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
