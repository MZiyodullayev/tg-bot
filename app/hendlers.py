from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

import app.keyboards as kb

router = Router()



@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Salom! Bot ishlayapti.", reply_markup=kb.main_menu)


@router.message(Command("profile"))
async def cmd_profile(message: Message):
    await message.reply(f"Salom, {message.from_user.first_name}!\nID: {message.from_user.id}",
    reply_markup=kb.settings)
    

@router.message(Command("help"))
async def help_command(message: Message):
    help_text = (
        "Bu bot sizga yordam berish uchun yaratilgan.\n"
        "Quyidagi buyruqlarni ishlatishingiz mumkin:\n"
        "/start - Botni ishga tushirish\n"
        "/help - Yordam haqida ma'lumot\n"
        "/profile - Sizning profilingiz haqida ma'lumot"
    )
    await message.reply(help_text)


@router.callback_query(F.data == "start")
async def callback_start(callback: CallbackQuery):
    await callback.answer('good', show_alert=True)
    await callback.message.edit_text("Salom! Bot ishlayapti.", reply_markup=await kb.inline_items())




    