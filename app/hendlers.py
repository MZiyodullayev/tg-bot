from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import app.keyboards as kb

router = Router()


# --- Состояния регистрации ---
class Registration(StatesGroup):
    full_name = State()
    phone = State()



# --- /start ---
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "🤖 Добро пожаловать!\n\n"
        "Нажмите кнопку ниже, чтобы начать.",
        reply_markup=kb.start_button
    )


# # --- /start ---
# @router.message(CommandStart())
# async def cmd_start(message: Message, state: FSMContext):
#     await state.clear()
#     await message.answer("Здравствуйте! Бот на связи.", reply_markup=kb.main_menu)


# --- Регистрация: начало ---
@router.callback_query(F.data == "register")
async def start_registration(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("📝 Регистрация началась.\n\nВведите ваше полное имя (ФИО):")
    await state.set_state(Registration.full_name)
    await callback.answer()


# --- Регистрация: получили ФИО ---
@router.message(Registration.full_name)
async def get_full_name(message: Message, state: FSMContext):
    name = message.text.strip()
    if len(name) < 3:
        await message.answer("❌ Имя слишком короткое. Пожалуйста, введите полное ФИ:")
        return

    await state.update_data(full_name=name)
    await message.answer(
        f"✅ Спасибо, {name}!\n\n📱 Теперь отправьте ваш номер телефона:",
        reply_markup=kb.phone_request
    )
    await state.set_state(Registration.phone)


# --- Регистрация: получили номер телефона ---
@router.message(Registration.phone, F.contact)
async def get_phone(message: Message, state: FSMContext):
    data = await state.get_data()
    full_name = data["full_name"]
    phone = message.contact.phone_number
    tg_id = message.from_user.id
    username = message.from_user.username or "нет"

    # Сохранить в файл (или замени на запрос к своему API)
    save_user(full_name, phone, tg_id, username)

    await message.answer(
        f"🎉 Регистрация успешно завершена!\n\n"
        f"👤 ФИ: {full_name}\n"
        f"📞 Телефон: {phone}\n"
        f"🆔 ID Telegram: {tg_id}",
        reply_markup=kb.remove_keyboard
    )
    await state.clear()


# --- Если прислал текст вместо кнопки на этапе телефона ---
@router.message(Registration.phone)
async def wrong_phone(message: Message):
    await message.answer(
        "❌ Пожалуйста, нажмите на кнопку ниже, чтобы отправить свой номер телефона 👇",
        reply_markup=kb.phone_request
    )


# --- /profile ---
# @router.message(Command("profile"))
# async def cmd_profile(message: Message):
#     await message.reply(
#         f"👤 {message.from_user.first_name}\n🆔 ID: {message.from_user.id}",
#         reply_markup=kb.settings
#     )


# --- /help ---
# @router.message(Command("help"))
# async def help_command(message: Message):
#     help_text = (
#         "Эти команды можно использовать:\n"
#         "/start — Запустить бота\n"
#         "/help — Помощь\n"
#         "/profile — Профиль"
#     )
#     await message.reply(help_text)


# --- Callback: profile ---
@router.callback_query(F.data == "profile")
async def callback_profile(callback: CallbackQuery):
    user = callback.from_user
    await callback.message.answer(
        f"👤 Имя: {user.first_name}\n"
        f"🆔 ID Telegram: {user.id}\n"
        f"📛 Username: @{user.username or 'нет'}",
        reply_markup=kb.settings
    )
    await callback.answer()


# --- Callback: help ---
@router.callback_query(F.data == "help")
async def callback_help(callback: CallbackQuery):
    help_text = (
        "ℹ️ Эти команды можно использовать:\n\n"
        "/start — Запустить бота\n"
        "/help — Помощь\n"
        "/profile — Профиль"
    )
    await callback.message.answer(help_text)
    await callback.answer()


# --- Callback: start ---
@router.callback_query(F.data == "start")
async def callback_start(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Здравствуйте! Бот на связи.", reply_markup=kb.main_menu)
    await callback.answer()


# --- Утилита: сохранение пользователя ---
def save_user(full_name: str, phone: str, tg_id: int, username: str):
    """
    Здесь можно:
    1. Сохранить в файл (сейчас так)
    2. Отправить POST запрос на сайт (раскомментируй ниже)
    3. Записать в базу данных
    """
    import json, os
    from datetime import datetime

    filepath = "users.json"
    users = []

    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            users = json.load(f)

    # Проверка дубликата
    for user in users:
        if user["tg_id"] == tg_id or user["phone"] == phone:
            return  # уже есть

    users.append({
        "full_name": full_name,
        "phone": phone,
        "tg_id": tg_id,
        "username": username,
        "registered_at": datetime.now().isoformat()
    })

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

    # --- Раскомментируй если есть API на сайте ---
    # import requests
    # requests.post("https://твой-сайт.com/api/register", json={
    #     "full_name": full_name,
    #     "phone": phone,
    #     "telegram_id": tg_id
    # })