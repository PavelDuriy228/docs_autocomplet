from maxapi import Router
from maxapi.types import MessageCreated, Command

router = Router(router_id="base_router")

# Здесь лежат общедоступные handlers


# Обработчик команды /start
@router.message_created(Command("start"))
async def start_handler(event: MessageCreated):
    await event.message.answer(f"Привет! {event.message}")


@router.message_created(Command("help"))
async def help_handler(event: MessageCreated):
    await event.message.answer("Помощь")
