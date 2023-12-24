from aiogram import executor
from dispatcher import dp
import handlers

from character import CharacterAI


async def on_startup(_: dp) -> None:
    CharacterAI().init()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
