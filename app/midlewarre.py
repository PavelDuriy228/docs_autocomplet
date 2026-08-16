from maxapi.filters.middleware import BaseMiddleware
from maxapi.types import MessageCreated

from typing import Any, Awaitable, Callable, Dict

from config import settings


class AccessControlMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[MessageCreated, Dict[str, Any]], Awaitable[Any]],
        event: MessageCreated,
        data: Dict[str, Any],
    ) -> Any:
        # Извлекаем ID отправителя из события
        user_id = event.message.sender.user_id

        # Проверяем, есть ли пользователь в белом списке
        if str(user_id) not in settings.ALLOWED_IDS:
            print(f"Доступ заблокирован для пользователя: {user_id}")
            await event.message.answer(
                f"Доступ заблокирован. Ваш id: {user_id} \nотправте его мне, чтобы я дал права"
            )
            return  # Прерываем цепочку. Хэндлер НЕ вызовется.

        # Если пользователь разрешен, передаем управление дальше
        return await handler(event, data)
