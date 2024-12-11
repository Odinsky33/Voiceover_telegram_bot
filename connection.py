from aiogram.fsm.storage.redis import RedisStorage
import redis
import asyncio

 
REDIS_URL = 'redis://127.0.0.1:6379/0'

storage = RedisStorage.from_url(REDIS_URL)

asyncio.run(storage.set_data())

