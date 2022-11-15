from aiogram.utils import executor

import handlers
from create_bot import dp

async def on_startup(_):
    print('Бот запущен')

handlers.registred_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)