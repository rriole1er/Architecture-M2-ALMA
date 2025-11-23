from __future__ import annotations

class User:
    """
    Gère les informations et comportements utilisateur.
    """
    def __init__(self, pseudo: str, password: str):
        self.pseudo = pseudo
        self.password = password
        self.friends = []
        self.inbox = []

    def setPseudo(self, pseudo: str):
        self.pseudo = pseudo

    def addFriend(self, u: 'User'):
        if u not in self.friends:
            self.friends.append(u)

    def removeFriend(self, u: 'User'):
        if u in self.friends:
            self.friends.remove(u)

    def receiveMessage(self, m: 'PrivateMessage'):
        self.inbox.append(m)

    def __repr__(self):
        return f"User({self.pseudo})"