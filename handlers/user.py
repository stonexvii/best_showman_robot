from datetime import date

from aiogram import Router, Bot, F
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import config
from ai_gpt import ai_client
from ai_gpt.enums import AIRole, GPTRole
from ai_gpt.gpt_client import GPTMessage
from fsm.states import UserDialog
from keyboards.inline_keyboards import ikb_message_link

user_router = Router()


@user_router.message(F.text, UserDialog.wait_for_answer)
async def text_messages(message: Message, bot: Bot, state: FSMContext):
    await bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
        request_timeout=10,
    )
    data = await state.get_data()
    keyboard = None
    msg_list = GPTMessage.from_json(data['messages'])
    my_message = message.text
    if data['count'] > config.MAX_MESSAGE:
        my_message = 'FINISH'
        await state.set_state(UserDialog.count_out_of_range)
        keyboard = ikb_message_link()
    msg_list.update(GPTRole.USER, my_message)
    response = await ai_client.request(msg_list)
    msg_list.update(GPTRole.CHAT, response)
    await state.update_data(
        {
            'messages': msg_list.json(),
            'count': data['count'] + 1
        }
    )
    await message.answer(
        text=response,
        reply_markup=keyboard,
    )


@user_router.message(UserDialog.count_out_of_range)
async def pause_handler(message: Message, bot: Bot, state: FSMContext):
    await bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
        request_timeout=10,
    )
    data = await state.get_data()
    current_date = date.today()
    if current_date > data['start_date']:
        await state.set_state(UserDialog.wait_for_answer)
        msg_list = GPTMessage(AIRole.SHOWMAN.value)
        msg_list.update(GPTRole.USER, message.text)
        await state.update_data(
            {
                'count': 0,
                'messages': msg_list.json(),
            }
        )
        await text_messages(message, bot, state)
    else:
        await message.answer(
            text='Превышен лимит токенов\nПриходите завтра!',
        )
