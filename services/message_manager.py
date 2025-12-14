from models.private_message import PrivateMessage
from models.user import User
from storage.storage import Storage


class MessageManager:
    """
    Gestion des messages privés.
    """
    def __init__(self, storage: Storage):
        self.storage = storage

    def sendPrivateMessage(self, sender: User, receiver: User, text: str):
        msg = PrivateMessage(sender, receiver, text)
        receiver.receiveMessage(msg)
        self.storage.save_message(msg)
        return msg

    def getInbox(self, user: User):
        messages = []
        for p in user.inbox:
            ts = p.timestamp.strftime("%H:%M")
            messages.append({
                "timestamp": ts,
                "sender": p.sender.pseudo,
                "content": p.content
            })
        return messages

    def getConversation(self, user1: User, user2: User):
        conversation = []
        for p in user1.inbox + user2.inbox:
            if (p.sender == user1 and p.receiver == user2) or (p.sender == user2 and p.receiver == user1):

                conversation.append({
                    "timestamp": p.timestamp.strftime("%H:%M"),
                    "sort_ts": p.timestamp,
                    "sender": p.sender.pseudo,
                    "content": p.content
                })
        conversation.sort(key=lambda x: x["sort_ts"])

        return conversation
