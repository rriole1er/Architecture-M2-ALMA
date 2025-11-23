from services.mininet_manager import MiniNetManager


class CLI:
    """
    Interface en ligne de commande pour MiniNet.
    """
    def __init__(self, system: MiniNetManager):
        self.sys = system
        self.current_user = None

    def menu(self):
        while True:
            if not self.current_user:
                print("\n--- MiniNet ---")
                print("1. Inscription")
                print("2. Connexion")
                print("0. Quitter")

                choice = input("> ")

                if choice == "1":
                    self.signup()
                elif choice == "2":
                    self.login()
                elif choice == "0":
                    break
            else:
                self.user_menu()

    def signup(self):
        try:
            pseudo = input("Pseudo: ")
            password = input("Mot de passe: ")

            user = self.sys.auth.signUp(pseudo, password)
            print("Inscription réussie.")
        except Exception as e:
            print("Erreur:", e)

    def login(self):
        try:
            pseudo = input("Pseudo: ")
            password = input("Mot de passe: ")

            self.current_user = self.sys.auth.logIn(pseudo, password)
            print(f"Bienvenue {self.current_user.pseudo}!")
        except Exception as e:
            print("Erreur:", e)

    def user_menu(self):
        print(f"\n--- Menu ({self.current_user.pseudo}) ---")
        print("1. Poster un message")
        print("2. Voir le fil d’actualité")
        print("3. Ajouter un ami")
        print("4. Voir mes amis")
        print("5. Envoyer un message privé")
        print("6. Voir mes messages")
        print("9. Déconnexion")

        choice = input("> ")

        if choice == "1":
            self.post()
        elif choice == "2":
            self.feed()
        elif choice == "3":
            self.add_friend()
        elif choice == "4":
            print(self.sys.userMgr.listFriends(self.current_user))
        elif choice == "5":
            self.send_pm()
        elif choice == "6":
            self.sys.msgMgr.getInbox(self.current_user)
        elif choice == "9":
            self.current_user = None

    def post(self):
        text = input("Texte: ")
        self.sys.postMgr.postMessage(self.current_user, text=text)
        print("Message posté.")

    def feed(self):
        self.sys.postMgr.getFeed(self.current_user)

    def add_friend(self):
        pseudo = input("Pseudo de l’ami: ")
        friend = self.sys.userMgr.getUser(pseudo)
        if not friend:
            print("Utilisateur introuvable.")
            return
        self.sys.userMgr.addFriend(self.current_user, friend)
        print("Ami ajouté.")

    def send_pm(self):
        pseudo = input("À : ")
        friend = self.sys.userMgr.getUser(pseudo)
        if not friend:
            print("Utilisateur introuvable.")
            return
        text = input("Message: ")
        self.sys.msgMgr.sendPrivateMessage(self.current_user, friend, text)
        print("Message envoyé.")