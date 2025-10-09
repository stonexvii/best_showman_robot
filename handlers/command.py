from datetime import date

from aiogram import Router, Bot
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ai_gpt import ai_client
from ai_gpt.enums import AIRole, GPTRole
from ai_gpt.gpt_client import GPTMessage
from fsm.states import UserDialog

command_router = Router()


@command_router.message(Command('start'))
async def command_start(message: Message, bot: Bot, state: FSMContext):
    await state.set_state(UserDialog.wait_for_answer)
    await bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
        request_timeout=10,
    )
    msg_list = GPTMessage(AIRole.SHOWMAN.value)
    msg_list.update(GPTRole.USER, f'Привет! Меня зовут {message.from_user.first_name}! А ты кто?')
    response = await ai_client.request(msg_list)
    msg_list.update(GPTRole.CHAT, response)
    await message.answer(
        text=response
    )
    await state.update_data(
        {
            'messages': msg_list.json(),
            'count': 1,
            'start_date': date.today(),
        }
    )
