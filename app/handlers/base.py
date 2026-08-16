from maxapi import Router, F
from maxapi.types import MessageCreated, Command
from maxapi.types.attachments.attachment import ButtonsPayload
from maxapi.types.attachments.buttons import MessageButton
from maxapi.enums.format import Format
from app.helpers.os_worker import get_student_dirs
from pipline import run_pipline

router = Router(router_id="base_router")

# Здесь лежат общедоступные handlers


# Обработчик команды /start
@router.message_created(Command("start"))
async def start_handler(event: MessageCreated):
    buttons = [
        [MessageButton(text="Получить архив документов")],
        [MessageButton(text="Какие студенты загружены")],
        [MessageButton(text="Обновить данные")],
        [MessageButton(text="Сводка по данным")],
    ]
    payload = ButtonsPayload(buttons=buttons).pack()

    await event.message.answer(
        text=f"Привет! \nНажмите на 'Получить архив документов'",
        attachments=[payload],
    )


@router.message_created(Command("help"))
async def help_handler(event: MessageCreated):
    await event.message.answer("Помощь")


@router.message_created(F.message.body.text == "Какие студенты загружены")
async def get_all_users(event: MessageCreated):
    student_dirs = get_student_dirs()
    text = f"Форму заполнили **{len(student_dirs)}** студентов: \n•{"\n•".join(student_dirs)}"
    await event.message.answer(text=text, format=Format.MARKDOWN)


@router.message_created(F.message.body.text == "Обновить данные")
async def data_update(event: MessageCreated):
    await event.message.answer(
        text=f"Начинаю обновление данных с формы, заполнение документов и отправку на диск",
    )

    res = await run_pipline()
    if res:
        await event.message.answer(text=f"Все готово!")
    else:
        await event.message.answer(text=f"Что то пошло не так")


@router.message_created(F.message.body.text == "Сводка по данным")
async def get_describe(event: MessageCreated):
    student_dirs = get_student_dirs()
    text = f"Какие студенты заполнилили форму: {len(student_dirs)}"
    await event.message.answer(text=text, format=Format.MARKDOWN)
