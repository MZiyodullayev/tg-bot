from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)

# main_menu = ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             KeyboardButton(text="/start"),
#             KeyboardButton(text="/help"),
#             KeyboardButton(text="/profile")
#         ]
#     ],
#     resize_keyboard=True,
#     input_field_placeholder="Menyu tanlang 👇"
# )

main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Start", callback_data="start")],
    [InlineKeyboardButton(text="Help", callback_data="help")],
    [InlineKeyboardButton(text="Profile", callback_data="profile")]
])


settings = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Поддержка", url="https://www.instagram.com/idk_mirmakhmud/")],
        [InlineKeyboardButton(text="Наш Сайт", url="https://www.buymeacoffee.com/idk_mirmakhmud")]])

items = ['Item 1', 'Item 2', 'Item 3']

async def inline_items():
    keyboard_rows = []
    row = []

    for index, item in enumerate(items, start=1):
        row.append(InlineKeyboardButton(text=item, callback_data=f"item_{item}"))
        if index % 2 == 0:
            keyboard_rows.append(row)
            row = []

    if row:
        keyboard_rows.append(row)

    return InlineKeyboardMarkup(inline_keyboard=keyboard_rows)