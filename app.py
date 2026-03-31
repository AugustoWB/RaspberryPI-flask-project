# Criado por Fernando Pozzer 2025
# Alterado por Rafael Reis 2026

from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3
import dataScr

#autenticação
from auth import auth, login_manager
from flask_login import login_required, current_user

app = Flask(__name__)
app.secret_key = "segredo"

# inicia login manager
login_manager.init_app(app)

# registra rotas de auth (login, signup, logout)
app.register_blueprint(auth)


#conexão com banco
def connect_db():
    return sqlite3.connect('data.db')


# API
@app.route('/', methods=['POST', 'GET'])
def use_api():
    try:
        if request.method == "POST":
            value = request.json.get('data')

            if value is None:
                return jsonify({"error": "No value provided"}), 400

            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO data (value) VALUES (?)',
                    (value,)
                )
                conn.commit()

            return jsonify({"message": "Value added successfully"}), 201

        elif request.method == "GET":
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM data')
                rows = cursor.fetchall()

            values = [{"id": row[0], "data": row[1]} for row in rows]
            return jsonify(values), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


#pags

@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/profile')
@login_required  
def profile():
    return render_template("profile.html", user=current_user.id)


# redirecionamento padrão
@app.route('/index')
def index():
    return redirect(url_for('home'))


#rodar app
if __name__ == '__main__':
    app.run(host="10.1.24.52", port=5000, debug=True)
