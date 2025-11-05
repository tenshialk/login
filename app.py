from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = "troque-esta-chave-por-uma-segura"  # use variável de ambiente em produção

# Usuários de exemplo (email → senha criptografada)
users = {
    "mariana@ifrn.edu.br": generate_password_hash("senha123")
}

# Decorador para proteger rotas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("Por favor, faça login para acessar essa página.")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


# Página inicial
@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/principal")
@login_required
def principal():
    email = session.get("user")
    return render_template("principal.html", email=email)

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Preencha e-mail e senha.")
            return render_template("login.html")

        user_hash = users.get(email)
        if user_hash and check_password_hash(user_hash, password):
            session["user"] = email
            flash("Login realizado com sucesso!")
            return redirect(url_for("principal"))
        else:
            flash("E-mail ou senha incorretos.")
            return render_template("login.html")

    return render_template("login.html")


# Página protegida
@app.route("/dashboard")
@login_required
def dashboard():
    email = session.get("user")
    return render_template("dashboard.html", email=email)


# Logout
@app.route("/logout")
@login_required
def logout():
    session.pop("user", None)
    flash("Você saiu com sucesso.")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
