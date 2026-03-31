from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import sqlite3

auth = Blueprint('auth', __name__)

login_manager = LoginManager()
login_manager.login_view = "auth.login"

# conexão
def connect_db():
    return sqlite3.connect('data.db')


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


#login
@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, password FROM users WHERE email = ?",
            (email,)
        )
        user = cursor.fetchone()
        conn.close()

        if user and user[1] == password:
            login_user(User(user[0]))
            return redirect(url_for("profile"))

    return render_template("login.html")


# signup
@auth.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = connect_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (email, password) VALUES (?, ?)",
                (email, password)
            )
            conn.commit()
        except:
            pass  # email já existe

        conn.close()
        return redirect(url_for("auth.login"))

    return render_template("signup.html")


# logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
