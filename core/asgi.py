# asgi.py
import os
import os
import environ
from pathlib import Path
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from core.websocket_urls import websocket_urlpatterns
#
import json

from channels.generic.http import AsyncHttpConsumer
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, types, enums
from asgiref.sync import sync_to_async
from apps.bot.models import TelegramBotConfiguration
from django.urls import path

from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from redis.asyncio.client import Redis
from apps.bot import handlers

base_dir = Path(__file__).resolve().parent.parent.parent
env = environ.Env()
env.read_env(os.path.join(base_dir, ".env"))

redis = Redis.from_url(env.str('REDIS_URL', 'redis://localhost:6379/0'))
dp = Dispatcher(storage=RedisStorage(redis=redis))

dp.include_routers(
    handlers.start_command.router,
    handlers.echo.router
)


class WebhookConsumer(AsyncHttpConsumer):
    async def handle(self, body):
        request_body = body.decode("utf-8")
        payload = json.loads(request_body)

        telegram_conf = await sync_to_async(TelegramBotConfiguration.get_solo)()
        bot = Bot(token=telegram_conf.token, default=DefaultBotProperties(parse_mode=enums.ParseMode.HTML))

        update = types.Update(**payload)

        await dp.feed_update(bot=bot, update=update)

        await self.send_response(
            status=200,
            body=b'{"message": "Hello, webhook is working!"}',
            headers=[(b"Content-Type", b"application/json")]
        )


#

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
application = ProtocolTypeRouter({
    "telegram": URLRouter([
        path("bot/webhook/", WebhookConsumer.as_asgi()),
    ]),
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),

})
