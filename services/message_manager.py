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
        for p in user.inbox:
            print(f"[{p.timestamp}] {p.sender.pseudo}: {p.content}")

        #print(self.storage.messages,"here")


