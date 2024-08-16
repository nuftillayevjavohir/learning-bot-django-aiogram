import json

from aiogram import types, Bot, enums
from aiogram.client.default import DefaultBotProperties

from asgiref.sync import sync_to_async

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import get_user_model

from core.asgi import dp

from apps.bot.models import TelegramBotConfiguration

User = get_user_model()


@method_decorator(csrf_exempt, name='dispatch')
class WebhookView(View):
    async def post(self, request: HttpRequest, *args, **kwargs):
        telegram_conf = await sync_to_async(TelegramBotConfiguration.get_solo)()
        bot = Bot(token=telegram_conf.token, default=DefaultBotProperties(parse_mode=enums.ParseMode.HTML))
        upd = types.Update(**(json.loads(request.body)))
        await dp.feed_update(bot=bot, update=upd)
        return HttpResponse('Hello, webhook is working!')

