from services.auth_manager import AuthenticationManager
from services.message_manager import MessageManager
from services.post_manager import PostManager
from services.user_manager import UserManager
from storage.storage import Storage


class MiniNetManager:
    """
    Point d’entrée : orchestre les services.
    """
    def __init__(self):
        self.storage = Storage()
        self.auth = AuthenticationManager(self.storage)
        self.userMgr = UserManager(self.storage)
        self.postMgr = PostManager(self.storage)
        self.msgMgr = MessageManager(self.storage)