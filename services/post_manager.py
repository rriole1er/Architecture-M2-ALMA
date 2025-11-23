from models.post import Post
from models.user import User
from storage.storage import Storage


class PostManager:
    """
    Gestion des posts.
    """
    def __init__(self, storage: Storage):
        self.storage = storage

    def postMessage(self, author: User, text=None, imageUrl=None, linkUrl=None):
        post = Post(author, text, imageUrl, linkUrl)
        self.storage.save_post(post)
        return post

    def getFeed(self, user: User):
        for p in self.storage.posts:
            if p.author == user or p.author in user.friends:
                print(f"[{p.timestamp}] {p.author.pseudo}: {p.text}")