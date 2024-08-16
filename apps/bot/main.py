from fastapi import FastAPI

from aiogram import types, Bot, enums
from aiogram.client.default import DefaultBotProperties

from asgiref.sync import sync_to_async

from django.contrib.auth import get_user_model

from apps.bot.bot_conf import dp
from apps.bot.models import TelegramBotConfiguration

User = get_user_model()

app = FastAPI()


@app.post("/bot/webhook/")
async def webhook(update: types.Update):
    telegram_conf = await sync_to_async(TelegramBotConfiguration.get_solo)()
    bot = Bot(token=telegram_conf.token, default=DefaultBotProperties(parse_mode=enums.ParseMode.HTML))
    await dp.feed_update(bot=bot, update=update)
    return {"message": "Hello, webhook is working!"}
