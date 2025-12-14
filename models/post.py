from datetime import datetime

from models.user import User


class Post:
    """
    Modèle d’un post utilisateur.
    """
    def __init__(self, author: User, text=None, imageUrl=None, linkUrl=None):
        self.id = id(self)
        self.text = text
        self.imageUrl = imageUrl
        self.linkUrl = linkUrl
        self.timestamp = datetime.now()
        self.author = author


def __repr__(self):
        return f"Post({self.author.pseudo}, {self.timestamp.strftime("%Y-%m-%d %H:%M:%S")})"