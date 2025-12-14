from models.post import Post
from models.user import User
from storage.storage import Storage


class PostManager:
    """
    Gestion des posts.
    """
    def __init__(self, storage: Storage):
        self.storage = storage

    def postMessage(self, author: User, text: str, imageUrl=None, linkUrl=None):
        post = Post(author, text, imageUrl, linkUrl)
        self.storage.save_post(post)
        return post

    def getFeed(self, user: User):
        all_posts = self.storage.posts or []
        friends = getattr(user, "friends", []) or []
        feed = [p for p in all_posts if p.author in friends or p.author == user]

        try:
            feed.sort(key=lambda p: p.timestamp, reverse=True)
        except Exception:
            pass

        # ajouter un attribut d'affichage sans secondes pour les templates
        for p in feed:
            p.display_timestamp = p.timestamp.strftime("%Y-%m-%d %H:%M")

        return feed