import secrets

from flask import Flask, flash, redirect, render_template, request, session, url_for
from time import time

from config import AppConfig

from src.models.mo_Usuario import mo_Usuario
from src.utils.decorators import login_required
from src.views.vi_UsuarioEX import main as usuario_blueprint
from src.views.vi_Monitoring import main as monitoring_blueprint
from src.views.farms.farm_view import main as farm_blueprint
from src.views.crops.crop_view import main as crop_blueprint

from src.models.entities import Usuario
from src.models.company_model import company_model

app = Flask(__name__, template_folder="src/templates", static_folder="src/static")
app.config.from_object(AppConfig)

app.register_blueprint(farm_blueprint, url_pefix="/")
app.register_blueprint(usuario_blueprint, url_prefix="/")
app.register_blueprint(monitoring_blueprint, url_prefix="/")
app.register_blueprint(crop_blueprint, url_prefix="/")


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
    #prueba()

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        ruc = request.form["ruc"]

        company = company_model.get_by_ruc(ruc)
        if company is None:
            flash("El RUC ingresado no se encuentra registrado.", "danger")
            return render_template("login.html")

        companyid = company["id"]

        autenticado, mensaje, datos_usuario = mo_Usuario.get_usuario(username, password, companyid)

        if autenticado:

            # Sesion unica por usuario: un nuevo login invalida la sesion anterior.
            session_token = secrets.token_urlsafe(32)
            if not mo_Usuario.set_active_session_token(datos_usuario["id"], session_token, datos_usuario["company_id"]):
                flash("No se pudo iniciar sesion en este momento. Intente nuevamente.", "danger")
                return render_template("login.html")
            print(datos_usuario["company_id"])
            session["usuario"] = {
                "id": datos_usuario["id"],
                "company_id": datos_usuario["company_id"],
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
    companyid = session.get("companyid")
    user_id = usuario.get("id")

    if user_id:
        mo_Usuario.clear_active_session_token(user_id, companyid, session_token=session_token)
    session.clear()
    return redirect(url_for("login"))


def prueba():
    admin = Usuario
    admin.username = "admin"
    admin.full_name = "perico de los palotes"
    admin.clave = "123456"
    admin.email = "admin@agrovision.ai"
    admin.rol = 1

    resultado = mo_Usuario.crear_usuario(admin)




if __name__ == "__main__":
    app.run(host=AppConfig.HOST, port=AppConfig.PORT, debug=AppConfig.DEBUG)
