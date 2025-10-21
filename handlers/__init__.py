from aiogram import Router

from .command import command_router
from .user import user_router

main_router = Router()

main_router.include_routers(
    command_router,
    user_router,

)
