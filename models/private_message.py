from __future__ import annotations
from datetime import datetime


class PrivateMessage:
    """
    Message privé entre utilisateurs.
    """

    def __init__(self, sender: User, receiver: User, content: str):
        self.id = id(self)
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.timestamp = datetime.now()

    def __repr__(self):
        return f"Message(from={self.sender.pseudo}, to={self.receiver.pseudo})"