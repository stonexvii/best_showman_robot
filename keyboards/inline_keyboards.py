from aiogram.utils.keyboard import InlineKeyboardBuilder


def ikb_message_link():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text='Перейти к комментариям',
        url=r'https://t.me/stone_event/20',
    )
    keyboard.adjust(1)
    return keyboard.as_markup()
