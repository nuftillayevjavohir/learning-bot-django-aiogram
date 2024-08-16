from aiogram import types, Router

router = Router()


@router.message()
async def echo(message: types.Message):
    await message.answer(message.text)
