from models.user import User
from storage.storage import Storage


class UserManager:
    """
    Gestion du réseau social (amis).
    """
    def __init__(self, storage: Storage):
        self.storage = storage

    def getUser(self, pseudo: str):
        return self.storage.get_user(pseudo)

    def addFriend(self, user: User, friend: User):
        user.addFriend(friend)
        friend.addFriend(user)

    def removeFriend(self, user: User, friend: User):
        user.removeFriend(friend)
        friend.removeFriend(user)

    def listFriends(self, user: User):
        return user.friends