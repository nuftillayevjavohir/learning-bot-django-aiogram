from core.asgi import application  # noqa

import os
import environ
from pathlib import Path
from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from redis.asyncio.client import Redis

from apps.bot import handlers

# READING ENV
base_dir = Path(__file__).resolve().parent.parent.parent
env = environ.Env()
env.read_env(os.path.join(base_dir, ".env"))

# GETTING WEBHOOK URL
webhook_path = '/telegram-bot/webhook/'
webhook_url = f"{env.str('BASE_URL', 'https://learning.jprq.app')}{webhook_path}"

redis = Redis.from_url(env.str('REDIS_URL', 'redis://localhost:6379/0'))
dp = Dispatcher(storage=RedisStorage(redis=redis))

dp.include_routers(
    ...
)
