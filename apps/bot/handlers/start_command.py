from aiogram import types, Router
from aiogram.filters.command import CommandStart

router = Router()


@router.message(CommandStart())
async def command_start(message: types.Message):
    await message.answer('Hello, world!')
