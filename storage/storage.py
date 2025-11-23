from models.post import Post
from models.private_message import PrivateMessage
from models.user import User


class Storage:
    """
    Stockage en mémoire (simple pour le prototype).
    """
    def __init__(self):
        self.users = {}      # pseudo → User
        self.posts = []      # List<Post>
        self.messages = []   # List<PrivateMessage>

    def save_user(self, user: User):
        self.users[user.pseudo] = user

    def get_user(self, pseudo: str):
        return self.users.get(pseudo)

    def save_post(self, post: Post):
        self.posts.append(post)

    def save_message(self, message: PrivateMessage):
        self.messages.append(message)
