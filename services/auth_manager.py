from models.user import User
from storage.storage import Storage


class AuthenticationManager:
    """
    Gestion de l’inscription et connexion.
    """
    def __init__(self, storage: Storage):
        self.storage = storage

    def logIn(self, pseudo: str, password: str):
        user = self.storage.get_user(pseudo)
        if not user:
            raise Exception("Utilisateur introuvable.")
        if user.password != password:
            raise Exception("Mot de passe incorrect.")
        return user


    def signUp(self, pseudo: str, password: str):
        if self.storage.get_user(pseudo):
            raise Exception("Pseudo déjà utilisé.")

        user = User(pseudo, password)
        self.storage.save_user(user)
        return user