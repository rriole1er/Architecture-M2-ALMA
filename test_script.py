from services.mininet_manager import MiniNetManager

def main():
    system = MiniNetManager()

    # ---- Création des utilisateurs ----
    print("\n=== Création des utilisateurs ===")
    user1 = system.auth.signUp("alice", "1234")
    user2 = system.auth.signUp("bob", "abcd")

    print("User1 =", user1)
    print("User2 =", user2)

    # ---- Ajout en amis ----
    print("\n=== Ajout en amis ===")
    system.userMgr.addFriend(user1, user2)
    print("Amis de Alice :", system.userMgr.listFriends(user1))
    print("Amis de Bob   :", system.userMgr.listFriends(user2))

    # ---- Posts ----
    print("\n=== Post de chaque utilisateur ===")
    system.postMgr.postMessage(user1, text="Bonjour, je suis Alice !")
    system.postMgr.postMessage(user2, text="Salut, Bob ici !")

    print("Fil de Alice :")
    system.postMgr.getFeed(user1)
    print("Fil de Bob   :")
    system.postMgr.getFeed(user2)

    # ---- Messages privés ----
    print("\n=== Échange de messages privés ===")
    system.msgMgr.sendPrivateMessage(user1, user2, "Salut Bob ! Comment ça va ?")
    system.msgMgr.sendPrivateMessage(user2, user1, "Très bien Alice, merci !")

    print("Inbox Alice :")
    system.msgMgr.getInbox(user1)
    print("Inbox Bob   :")
    system.msgMgr.getInbox(user2)

    print("\n=== FIN DU TEST ===")

if __name__ == "__main__":
    main()