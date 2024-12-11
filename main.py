import asyncio
import logging
from aiogram import Bot, Dispatcher
from app.handlers import router

BOT_TOKEN = "5845147186:AAEtNTDf1_iuqa0FyDgXhRB41lBENwvG0XE"

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=BOT_TOKEN)
# Диспетчер
dp = Dispatcher()



# Запуск процесса поллинга новых апдейтов
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())