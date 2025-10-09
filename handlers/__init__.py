from aiogram import Router

from .admin import admin_router
from .command import command_router
from .user import user_router

main_router = Router()

main_router.include_routers(
    admin_router,
    command_router,
    user_router,
)
