from functools import wraps
from time import time

from flask import abort, jsonify, redirect, request, session, url_for
from config import AppConfig
from src.models.mo_Usuario import mo_Usuario


def _unauthorized_response():
    wants_json = request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest"
    accepts_json = request.accept_mimetypes["application/json"] >= request.accept_mimetypes["text/html"]

    if wants_json or accepts_json:
        return jsonify({"success": False, "error": "Sesión expirada o acceso no autorizado"}), 401

    return redirect(url_for("login"))


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = session.get("usuario")
        if not user or not user.get("autenticado"):
            return _unauthorized_response()

        user_id = user.get("id")
        current_token = session.get("session_token")
        if not user_id or not current_token:
            session.clear()
            return _unauthorized_response()

        active_token = mo_Usuario.get_active_session_token(user_id)
        if not active_token or active_token != current_token:
            session.clear()
            return _unauthorized_response()

        now = int(time())
        last_activity = session.get("last_activity")
        timeout_seconds = AppConfig.SESSION_TIMEOUT_HOURS * 3600

        # Si no hay marca de actividad previa o si expiró, forzamos cierre de sesión.
        if not isinstance(last_activity, int):
            session.clear()
            return _unauthorized_response()

        if now - last_activity > timeout_seconds:
            session.clear()
            return _unauthorized_response()

        # Timeout por inactividad: cada request válida renueva la marca de tiempo.
        session["last_activity"] = now
        session.modified = True
        return f(*args, **kwargs)

    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = session.get("usuario")
        if not user or not user.get("autenticado"):
            return _unauthorized_response()
        if user.get("rol") != 1:
            abort(403)
        return f(*args, **kwargs)

    return wrapper


def admin_or_owner_required(param_id_key='id'):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = session.get('usuario')
            if not user or not user.get("autenticado"):
                return _unauthorized_response()

            is_admin = user.get('rol') == 1
            session_user_id = user.get('id')

            # Obtener ID del request.args (GET) o kwargs
            requested_id = None
            if param_id_key in kwargs:
                requested_id = kwargs.get(param_id_key)
            elif param_id_key in session:
                requested_id = session.get(param_id_key)
            else:
                from flask import request
                requested_id = request.args.get(param_id_key, type=int)

            # Seguridad: Admin o el dueño de su propio perfil
            if not is_admin and requested_id != session_user_id:
                abort(403)
            return f(*args, **kwargs)
        return wrapper
    return decorator
