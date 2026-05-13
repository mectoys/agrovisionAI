from flask import Blueprint, jsonify, render_template, request, session

from src.models.mo_Usuario import mo_Usuario
from src.models.entities.Usuario import Usuario
from src.utils.decorators import admin_required, login_required


main = Blueprint('bp_usuario', __name__)


def Obtener_usuarios_data_form_request():
    data = request.get_json()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    rol = data.get('rol')
    clave = data.get('clave', '').strip()

    if not username or not email or not rol:
        raise ValueError("Faltan campos obligatorios")

    return username, clave, email, rol


@main.route('/usuario')
@admin_required
def lista_Usuario():
    usuarios = mo_Usuario.get_usuarios()
    return render_template(
        '/users/user_List.html',
        usuarios=usuarios,
        use_datatables=True,
        use_visitorcss=False,
    )


@main.route('/usuario/page_user')
@admin_required
def usuario_form_page():
    iduser = request.args.get('id', type=int)
    usuario = mo_Usuario.get_oneUser(iduser) if iduser else None
    return render_template(
        '/users/user_form.html',
        use_datatables=True,
        use_visitorcss=False,
        usuario=usuario,
    )


@main.route('/usuario/page', methods=['POST'])
@admin_required
def usuario_form_action():
    try:
        data = request.get_json()
        iduser = int(data.get('iduser', 0))
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        clave = data.get('clave', '')
        reclave = data.get('reclave', '')
        rol = data.get('rol')

        if not username or not email or not rol:
            return jsonify({"success": False, "error": "Campos obligatorios incompletos"}), 400

        if clave != reclave:
            return jsonify({"success": False, "error": "Las contraseñas no coinciden"}), 400

        usuario_obj = Usuario(username, '', clave, email, rol, iduser if iduser is not None else 0)

        if iduser:
            result = mo_Usuario.editar_usuario(usuario_obj)
            message = "Usuario actualizado correctamente"
        else:
            result = mo_Usuario.crear_usuario(usuario_obj)
            message = "Usuario creado correctamente"

        if result.get("success"):
            return jsonify({"success": True, "message": message}), 200
        return jsonify({"success": False, "error": result.get("error", "Error desconocido")}), 409

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@main.route('/usuario/password')
@login_required
def usuario_mostraractualizapassword():
    iduser = request.args.get('id', type=int)
    if not iduser:
        iduser = session.get('usuario', {}).get('id')
    usuario = mo_Usuario.get_oneUser(iduser) if iduser else None

    return render_template(
        '/users/user_updatePassword.html',
        usuario=usuario,
        use_datatables=False,
        use_visitorcss=False,
    )


@main.route('/usuario/update_password', methods=['POST'])
@login_required
def update_password():
    usuario_id = session.get('usuario', {}).get('id')
    if not usuario_id:
        return jsonify({"success": False, "error": "Sesión expirada o no válida"}), 401

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No se recibieron datos"}), 400

    current_pass = data.get('current_pass')
    new_pass = data.get('new_pass')

    if not current_pass or not new_pass:
        return jsonify({"success": False, "error": "Todos los campos son obligatorios"}), 400

    try:
        exito, mensaje = mo_Usuario.actualizar_password(usuario_id, current_pass, new_pass)

        if exito:
            return jsonify({"success": True, "message": mensaje}), 200
        return jsonify({"success": False, "error": mensaje}), 400

    except Exception as e:
        print(f"Error critico en vista update_password: {e}")
        return jsonify({"success": False, "error": "Error interno al procesar la solicitud"}), 500


