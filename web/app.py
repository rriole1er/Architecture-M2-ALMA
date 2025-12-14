from time import sleep

from flask import Flask, render_template, request, redirect, session
from services.mininet_manager import MiniNetManager
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "mininet-secret"

system = MiniNetManager()

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
app.config["UPLOAD_FOLDER"] = os.path.abspath(UPLOAD_FOLDER)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# ---------- DATA SEED (pré-remplissage) ----------
def seed_data():
    try:
        alice = system.auth.signUp("alice", "1234")
        bob = system.auth.signUp("bob", "abcd")
        eve = system.auth.signUp("eve", "pass")

        system.userMgr.addFriend(alice, bob)
        system.userMgr.addFriend(bob, alice)
        system.userMgr.addFriend(alice, eve)
        system.userMgr.addFriend(eve,alice)

        system.postMgr.postMessage(alice, "Bonjour, je suis Alice !", imageUrl="https://storage.googleapis.com/endurance-apps-liip/media/cache/disney_no_filter_grid_fs/594540e561cb7d3c2e8b45e0", linkUrl="https://alice.example.com")
        system.postMgr.postMessage(bob, "Salut, ici Bob !", imageUrl="https://stock.wikimini.org/w/images/4/4d/Bob_l%27%C3%A9ponge-Personnage.jpg", linkUrl="https://bob.example.com")
        system.postMgr.postMessage(eve, "Coucou, Eve à l'appareil.")


        system.msgMgr.sendPrivateMessage(alice, bob, "Salut Bob ! Comment ça va ?")
        sleep(1)
        system.msgMgr.sendPrivateMessage(bob, alice, "Très bien Alice, merci !")
        sleep(1)
        system.msgMgr.sendPrivateMessage(eve, alice, "Hello Alice, ça te dit de faire la connaissance ?")

        print("[SEED] Données de test ajoutées avec succès.")
    except Exception as e:
        # Cela évite les doublons si Flask recharge deux fois
        print("[SEED] Skipped:", e)

seed_data()

def current_user():
    pseudo = session.get("user")
    if not pseudo:
        return None
    return system.userMgr.getUser(pseudo)

# -------------------------
# Login / Signup
# -------------------------

@app.route("/")
def home():
    if not current_user() or current_user()!="User(alice)":
        return redirect("/login")
    return redirect("/feed")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pseudo = request.form["pseudo"]
        password = request.form["password"]
        try:
            user = system.auth.logIn(pseudo, password)
            session["user"] = user.pseudo
            return redirect("/feed")
        except Exception as e:
            return render_template("login.html", error=str(e))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        pseudo = request.form["pseudo"]
        password = request.form["password"]
        try:
            system.auth.signUp(pseudo, password)
            return redirect("/login")
        except Exception as e:
            return render_template("signup.html", error=str(e))
    return render_template("signup.html")


# -------------------------
# Feed & Posts
# -------------------------

@app.route("/feed")
def feed():
    user = current_user()
    if not user:
        return redirect("/login")

    posts = system.postMgr.getFeed(user)

    return render_template("feed.html", user=user, posts=posts)

@app.route("/post", methods=["GET", "POST"])
def post():
    user = current_user()
    if not user:
        return redirect("/login")

    if request.method == "POST":        #TO DO working with image upload + conception + comment
        text = request.form.get("text", "")
        # priorité : fichier uploadé, sinon URL fournie
        image_file = request.files.get("imageFile")
        imageUrl = None
        if image_file and image_file.filename:
            if allowed_file(image_file.filename):
                os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
                filename = secure_filename(image_file.filename)
                save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                image_file.save(save_path)
                # URL relative accessible via /static/...
                imageUrl = "/static/uploads/" + filename
            else:
                # optionnel : gérer erreur d'extension (ici on ignore si non autorisée)
                imageUrl = None
        else:
            imageUrl = request.form.get("imageUrl") or None

        linkUrl = request.form.get("linkUrl") or None
        system.postMgr.postMessage(user, text=text, imageUrl=imageUrl, linkUrl=linkUrl)
        return redirect("/feed")

    return render_template("post.html", user=user)


# -------------------------
# Messages privés
# -------------------------

@app.route("/inbox")
def inbox():
    user = current_user()
    if not user:
        return redirect("/login")

    messages = system.msgMgr.getInbox(user)

    return render_template("inbox.html", user=user, messages=messages)

@app.route("/send_message", methods=["POST"])
def send_message():
    user = current_user()
    if not user:
        return redirect("/login")

    to = request.form["to"]
    text = request.form["text"]
    receiver = system.userMgr.getUser(to)

    if receiver:
        system.msgMgr.sendPrivateMessage(user, receiver, text)

    return redirect("/conversation/" + to)

@app.route("/conversation/<pseudo>")
def conversation(pseudo):
    user = current_user()
    if not user:
        return redirect("/login")

    other_user = system.userMgr.getUser(pseudo)
    if not other_user:
        return redirect("/inbox")

    conversation = system.msgMgr.getConversation(user, other_user) or []
    other_user_name = other_user.pseudo

    return render_template(
        "conversation.html",
        user=user,
        other_user=other_user_name,
        conversation=conversation,
    )

# -------------------------
# Amis
# -------------------------

@app.route("/friends")
def friends():
    user = current_user()
    if not user:
        return redirect("/login")

    friends = system.userMgr.listFriends(user)
    return render_template("friends.html", user=user, friends=friends)

@app.route("/add_friend", methods=["POST"])
def add_friend():
    user = current_user()
    if not user:
        return redirect("/login")

    friend_pseudo = request.form["pseudo"]

    if friend_pseudo == user.pseudo:
        return render_template("friends.html", user=user, friends=system.userMgr.listFriends(user), error="Vous ne pouvez pas vous ajouter vous-même en ami.")

    friend = system.userMgr.getUser(friend_pseudo)

    if friend and friend in system.userMgr.listFriends(user):
        return render_template("friends.html", user=user, friends=system.userMgr.listFriends(user), error="Cet utilisateur est déjà dans votre liste d'amis.")

    if friend:
        system.userMgr.addFriend(user, friend)
        return redirect("/friends")

    else :
        return render_template("friends.html", user=user, friends=system.userMgr.listFriends(user), error="Utilisateur introuvable.")

#delete friend route
@app.route("/delete_friend", methods=["POST"])
def delete_friend():
    user = current_user()
    if not user:
        return redirect("/login")

    friend_pseudo = request.form["friend_id"]
    friend = system.userMgr.getUser(friend_pseudo)

    print(friend_pseudo)
    print("Friend to delete:", friend)


    if friend and friend in system.userMgr.listFriends(user):
        system.userMgr.removeFriend(user, friend)
        return redirect("/friends")
    else:
        return render_template("friends.html", user=user, friends=system.userMgr.listFriends(user), error="Utilisateur introuvable ou pas dans votre liste d'amis.")



# -------------------------
# Run
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)
