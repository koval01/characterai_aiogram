from characterai import PyCAI

import config


class CharacterAI:
    client: PyCAI | dict = {}
    chat: PyCAI.chat | dict = {}
    
    def __init__(self) -> None:
        self.participants: list = self.chat.get("participants")
        self.external_id: str = self.chat.get("external_id")
        
    @property
    def tgt(self) -> str:
        if not self.participants[0]['is_human']:
            return self.participants[0]['user']['username']
        else:
            return self.participants[1]['user']['username']
    
    def init(self) -> None:
        CharacterAI.client = PyCAI(config.CHARACTERAI_TOKEN)
        CharacterAI.chat = self.client.chat.new_chat(config.CHARACTER_ID)
        
    def send(self, message: str) -> str | None:
        response: dict = self.client.chat.send_message(
            self.external_id, self.tgt, message
        )
        
        if "replies" not in response.keys():
            return
        
        replies = response["replies"]
        if not replies:
            return
        
        return replies[0].get("text")
