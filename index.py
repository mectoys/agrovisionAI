import secrets

from flask import Flask, flash, redirect, render_template, request, session, url_for
from time import time

from config import AppConfig

from src.models.mo_Usuario import mo_Usuario
from src.utils.decorators import login_required
from src.views.vi_UsuarioEX import main as usuario_blueprint

from src.models.entities import Usuario

app = Flask(__name__, template_folder="src/templates", static_folder="src/static")
app.config.from_object(AppConfig)


app.register_blueprint(usuario_blueprint, url_prefix="/")
#app.register_blueprint(vi_VisitaEX.main, url_prefix="/")
#app.register_blueprint(vi_GetauxiliaryData.main, url_prefix="/")


@app.route("/")
@login_required
def index():

    return render_template(
        "index.html",
        use_datatables=False,
        username=session["usuario"]["username"],
        rol=session["usuario"].get("rol", 2),
    )


@app.route("/login", methods=["GET", "POST"])
def login():
   # prueba()

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        autenticado, mensaje, datos_usuario = mo_Usuario.get_usuario(username, password)

        if autenticado:

            # Sesion unica por usuario: un nuevo login invalida la sesion anterior.
            session_token = secrets.token_urlsafe(32)
            if not mo_Usuario.set_active_session_token(datos_usuario["id"], session_token):
                flash("No se pudo iniciar sesion en este momento. Intente nuevamente.", "danger")
                return render_template("login.html")

            session["usuario"] = {
                "id": datos_usuario["id"],
                "username": datos_usuario["username"],
                "rol": datos_usuario["rol_id"],
                "autenticado": True,
            }
            session["session_token"] = session_token
            session["last_activity"] = int(time())
            session.permanent = True
            return redirect(url_for("index"))

        flash(mensaje, "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    usuario = session.get("usuario", {})
    session_token = session.get("session_token")
    user_id = usuario.get("id")
    if user_id:
        mo_Usuario.clear_active_session_token(user_id, session_token=session_token)
    session.clear()
    return redirect(url_for("login"))


def prueba():
    admin = Usuario
    admin.username = "admin"
    admin.full_name="perico de los palotes"
    admin.clave = "123456"
    admin.email = "admin@agrovision.ai"
    admin.rol = 1

    resultado = mo_Usuario.crear_usuario(admin)

    print(resultado)


if __name__ == "__main__":
    app.run(host=AppConfig.HOST, port=AppConfig.PORT, debug=AppConfig.DEBUG)
