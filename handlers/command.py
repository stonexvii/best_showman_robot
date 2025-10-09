import os

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ai_gpt import ai_client
from ai_gpt.enums import AIRole, GPTRole
from ai_gpt.gpt_client import GPTMessage
from fsm.states import UserDialog
from classes.file_manager import FileManager
from classes.resources_paths import TEXT_MESSAGES

command_router = Router()


@command_router.message(Command('start'))
async def command_start(message: Message, state: FSMContext):
    user_name = message.from_user.full_name
    if user_name:
        start_message = f'Привет! Меня зовут {user_name}. Расскажи, кто ты, что ты умеешь и о чем я могу тебя спрашивать'
    else:
        start_message = 'Привет!'
    message_list = GPTMessage(AIRole.ASSISTANT.value)
    message_list.update(GPTRole.USER, start_message)
    response = await ai_client.request(message_list)
    message_list.update(GPTRole.CHAT, response)
    await message.answer(
        text=response,
    )
    await state.set_state(UserDialog.wait_for_answer)
    await state.update_data({'messages': message_list.json()})



@command_router.message(Command('rules'))
async def command_start(message: Message):
    await message.answer(
        text=FileManager.read_txt(os.path.join(TEXT_MESSAGES, 'bot_rules')),
    )


@command_router.message(Command('help'))
async def command_start(message: Message):
    await message.answer(
        text=FileManager.read_txt(os.path.join(TEXT_MESSAGES, 'bot_help')),
    )
