
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardRemove
)
 

start_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🚀 Начать", callback_data="start")]
])

# Главное меню (inline)
main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📝 Регистрация", callback_data="register")],
    [InlineKeyboardButton(text="👤 Профиль", callback_data="profile")],
    [InlineKeyboardButton(text="Помощь", callback_data="help")],
])
 
# Кнопка для передачи номера телефона
phone_request = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Оправить номер телефона", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
 
# Убрать клавиатуру
remove_keyboard = ReplyKeyboardRemove()
 
# Настройки / поддержка
settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🆘 Поддержка", url="https://www.instagram.com/idk_mirmakhmud/")],
    [InlineKeyboardButton(text="🌐 Наш сайт", url="https://www.buymeacoffee.com/idk_mirmakhmud")],
])
 