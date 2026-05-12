from flask import render_template, Blueprint, request, redirect, url_for, jsonify, session
from src.models.mo_Usuario import mo_Usuario
from src.models.entities.Usuario import Usuario
from src.utils.decorators import admin_required, login_required

main = Blueprint('bp_usuario', __name__)


#Funcion Auxiliar
# mo_Usuario.crear_usuario('admin', 'admin123', 'mectoys2013@gmail.com', 1)
def Obtener_usuarios_data_form_request():
  # El método.strip() en Python es una función útil para limpiar cadenas de texto eliminando caracteres no deseados
  # (como espacios en blanco o caracteres específicos) del inicio y final de una cadena.

    data = request.get_json()
    username = data.get('username', '').strip()  # Campo obligatorio
    email = data.get('email', '').strip()        # Campo obligatorio
    rol = data.get('rol')                        # Campo obligatorio (número)
    clave = data.get('clave', '').strip()        # Campo opcional

    # Validar campos obligatorios
    if not username or not email or not rol:
        raise ValueError("Faltan campos obligatorios")

    return username, clave, email, rol

#Método Listado de Usuarios
@main.route('/usuario')
@admin_required
def lista_Usuario():
    usuarios = mo_Usuario.get_usuarios()
    return render_template('/users/user_List.html', usuarios=usuarios, use_datatables=True,
                           use_visitorcss=False)

#Método que redirige a la pagina de Crear/Editar  Usuario
@main.route('/usuario/page_user')
@admin_required
def usuario_form_page():
    id = request.args.get('id', type=int)
    usuario = mo_Usuario.get_oneUser(id) if id else None
    return render_template('/users/user_form.html', use_datatables=True,use_visitorcss=False,
                           usuario=usuario)
####################NUEVA PROPUESTA
@main.route('/usuario/page', methods=['POST'])
@admin_required
def usuario_form_action():
    from src.models.entities.Usuario import Usuario

    try:
        data = request.get_json()
        iduser = int(data.get('iduser', 0))  # Siempre convertir a entero
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        clave = data.get('clave', '')
        reclave = data.get('reclave', '')
        rol = data.get('rol')

        # Validación
        if not username or not email or not rol:
            return jsonify({"success": False, "error": "Campos obligatorios incompletos"}), 400

        if clave != reclave:
            return jsonify({"success": False, "error": "Las contraseñas no coinciden"}), 400

        # Construcción del objeto (✅ sin forzar int)
        usuario_obj = Usuario(username, clave, email, rol, iduser if iduser is not None else 0)

        # Insertar o actualizar
        if iduser:  # Modo edición
            result = mo_Usuario.editar_usuario(usuario_obj)
            message = "Usuario actualizado correctamente"
        else:  # Modo inserción
            result = mo_Usuario.crear_usuario(usuario_obj)
            message = "Usuario creado correctamente"

        # Respuesta
        if result.get("success"):
            return jsonify({"success": True, "message": message}), 200
        else:
            return jsonify({"success": False, "error": result.get("error", "Error desconocido")}), 409

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

#Actualizar Contraseña
@main.route('/usuario/password')
@login_required
def usuario_mostraractualizapassword():
    id = request.args.get('id', type=int)
    if not id:
        id = session.get('usuario', {}).get('id')
    usuario = mo_Usuario.get_oneUser(id) if id else None

    return render_template('/users/user_updatePassword.html', usuario=usuario, use_datatables=False ,
                           use_visitorcss=False)


@main.route('/usuario/update_password', methods=['POST'])
@login_required
def update_password():
    # 1. Validación de Sesión Robusta
    # Es mejor verificar el ID directamente para asegurar que la sesión es válida y tiene datos
    usuario_id = session.get('usuario', {}).get('id')
    if not usuario_id:
        return jsonify({"success": False, "error": "Sesión expirada o no válida"}), 401

    # 2. Validación de Entrada (Evita que el sistema procese basura)
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No se recibieron datos"}), 400

    current_pass = data.get('current_pass')
    new_pass = data.get('new_pass')

    if not current_pass or not new_pass:
        return jsonify({"success": False, "error": "Todos los campos son obligatorios"}), 400

    # 3. Lógica de Negocio (Delegada al Modelo)
    try:
        exito, mensaje = mo_Usuario.actualizar_password(usuario_id, current_pass, new_pass)

        if exito:
            # 200 OK: Éxito total
            print('a')
            return jsonify({"success": True, "message": mensaje}), 200
        else:
            # 400 Bad Request: Error de lógica (ej. clave actual incorrecta)
            print('b')
            return jsonify({"success": False, "error": mensaje}), 400

    except Exception as e:
        # 4. Capa de Seguridad Final (Incluso si el modelo falla sin control)
        # Aquí es donde entraría tu nuevo sistema de LOGS
        print(f"Error crítico en vista update_password: {e}")
        return jsonify({"success": False, "error": "Error interno al procesar la solicitud"}), 500

