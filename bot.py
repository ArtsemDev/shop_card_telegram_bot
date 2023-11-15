from settings import bot, dp
from handlers.users import router


if __name__ == '__main__':
    dp.include_router(router=router)
    dp.run_polling(bot)
