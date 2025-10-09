from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ai_gpt import ai_client
from ai_gpt.enums import GPTRole
from ai_gpt.gpt_client import GPTMessage
from fsm.states import UserDialog

fsm_router = Router()


@fsm_router.message(F.text == 'clear', UserDialog.wait_for_answer)
async def user_clear_dialog(message: Message, bot: Bot, state: FSMContext):
    await state.clear()
    await message.answer(
        text='Ок, давай начнем все сначала! Введи команду /start'
    )


@fsm_router.message(UserDialog.wait_for_answer)
async def user_dialog(message: Message, bot: Bot, state: FSMContext):
    state_data = await state.get_value('messages')
    message_list = GPTMessage.from_json(state_data)
    message_list.update(GPTRole.USER, message.text)
    response = await ai_client.request(message_list)
    await message.answer(
        text=response,
    )
    message_list.update(GPTRole.CHAT, response)
    await state.update_data({'messages': message_list.json()})
