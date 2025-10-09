from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

import config
from ai_gpt.enums import AIRole
from classes.file_manager import FileManager
from classes.resources_paths import AI_PROMPTS_PATH
from middleware.admin import AdminMiddleware

admin_router = Router()
admin_router.message.middleware(AdminMiddleware())


@admin_router.message(Command('set_prompt'))
async def command_prompt(message: Message, command: CommandObject):
    full_path: str = AI_PROMPTS_PATH + AIRole.SHOWMAN.value
    FileManager.write_txt(full_path, command.args)
    await message.answer(
        text='Промпт установлен!'
    )


@admin_router.message(Command('set_count'))
async def command_count(message: Message, command: CommandObject):
    if command.args and command.args.isdigit():
        config.ANTI_SPAM_MINUTES = int(command.args)
        await message.answer(
            text=f'Установлено {command.args} сообщений в день!',
        )
