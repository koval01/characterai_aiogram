from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.utils.exceptions import CantParseEntities

import config


class IsOwnerFilter(BoundFilter):
    """
    Custom filter "is_owner".
    """
    key = "is_owner"

    def __init__(self, is_owner) -> None:
        self.is_owner = is_owner

    async def check(self, message: types.Message) -> bool:
        return message.from_user.id in config.BOT_OWNERS


class IsBotMention(BoundFilter):
    """
    Custom filter "is_bot_mention"
    """
    key = "is_bot_mention"

    def __init__(self, is_bot_mention) -> None:
        self.is_bot_mention = is_bot_mention

    async def check(self, message: types.Message) -> bool:
        try:
            entities = dict(message).get("entities")
        except CantParseEntities:
            return False

        if not entities:
            return False

        mention_objects = [m for m in entities if m["type"] == "mention"]

        username = config.USERNAME

        for mention_in_text in mention_objects:
            offset = mention_in_text["offset"]
            length = mention_in_text["length"]

            if message.text[offset:offset+length] == username:
                return True

        return False


class IsReplyBot(BoundFilter):
    """
    Custom filter "is_reply_bot"
    """
    key = "is_reply_bot"

    def __init__(self, is_reply_bot) -> None:
        self.is_reply_bot = is_reply_bot

    async def check(self, message: types.Message) -> bool:
        if message.reply_to_message:
            return message.reply_to_message.from_user.username == config.USERNAME[1:]
