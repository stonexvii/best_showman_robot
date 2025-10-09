import asyncio
import random

from aiogram import Router, Bot, F
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import config
from ai_gpt import ai_client
from ai_gpt.enums import AIRole
from ai_gpt.gpt_client import GPTMessage
from ai_gpt.enums import AIRole, GPTRole

user_router = Router()


@user_router.channel_post()
async def catch_id(message: Message, bot: Bot):
    msg_list = GPTMessage(AIRole.MODERATOR.value)
    msg_list.update(GPTRole.USER, message.text)
    response = await ai_client.request(msg_list)
    await bot.send_message(
        chat_id=message.chat.id,
        text=response,
    )


@user_router.message(F.text)
async def text_messages(message: Message, bot: Bot, state: FSMContext):
    await bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
    )
    response = await ai_client.request(AIRole.MODERATOR, message.text)
    verdict, content = response.split('\n', 1)

    await message.answer(
        text=content.strip(),
    )
    if verdict == 'Correct':
        await asyncio.sleep(random.randint(5, 10))
        await bot.send_message(
            chat_id=config.CHANNEL_ID,
            text=message.text,
        )
