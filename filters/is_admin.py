from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from core.utils.database import User, session

__all__ = ["IsAdmin"]


class IsAdmin(BaseFilter):

    async def __call__(self, update: Message | CallbackQuery) -> bool:
        with session() as s:
            user = s.get(User, update.from_user.id)
            if user is not None:
                if user.is_admin:
                    return True
                return False
            return False
