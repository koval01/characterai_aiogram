import asyncio

from aiogram import types
from aiogram.types import ContentType, ChatType, ChatActions
from dispatcher import dp, bot

from character import CharacterAI


def remove_entities(message: types.Message) -> types.Message:
    entities = dict(message).get("entities")

    if not entities:
        return message

    g_offset = 0
    for entity in entities:
        if entity["type"] in ["url", "mention"]:
            offset = entity["offset"]
            length = entity["length"]
            message.text = message.text[:offset-g_offset] + message.text[(offset-g_offset)+length:]
            g_offset += length

    return message


async def typing_loop(message: types.Message) -> None:
    for i in range(100):
        await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
        await asyncio.sleep(3.5)


async def get_response(message: types.Message) -> None:
    future = asyncio.ensure_future(typing_loop(message))
    message = remove_entities(message)
    await message.reply(CharacterAI().send(message.text))
    future.cancel()


@dp.message_handler(
    is_bot_mention=True,
    chat_type=[ChatType.SUPERGROUP, ChatType.GROUP],
    content_types=ContentType.TEXT
)
async def mention_in_chat(message: types.Message) -> None:
    await get_response(message)


@dp.message_handler(
    is_reply_bot=True,
    chat_type=[ChatType.SUPERGROUP, ChatType.GROUP],
    content_types=ContentType.TEXT
)
async def reply_in_chat(message: types.Message) -> None:
    await get_response(message)
