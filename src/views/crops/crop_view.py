from flask import Blueprint, jsonify, render_template, request, session

from src.models.crop_model import crop_model
from src.models.entities.crop import crop
from src.utils.decorators import admin_required, login_required

main = Blueprint('bp_crop', __name__)


#Obtener datos de usuario por sesion
def ObtainUserId():
    usuario = session.get('usuario')
    if not usuario:
        return jsonify([]), 401
    id_user = usuario.get('id')
    return id_user


def ObtainCompanyId():
    usuario = session.get('usuario')

    if not usuario:
        return jsonify([]), 401
    id_company = usuario.get('company_id')
    return id_company


@main.route('/crops')
@login_required
def list_crops():
    return render_template(
        '/crops/list.html',
        use_datatables=True,
        use_visitorcss=False,
    )


#Cargar listado de Cultivos Farms
@main.route('/crops/data')
@login_required
def Crops_data():
    id_company = ObtainCompanyId()
    crops = crop_model.get_crops(id_company)

    for v in crops:
        # Formateo fecha creacion
        if v['fecha_creacion']:
            v['fecha_creacion'] = v['fecha_creacion'].strftime("%Y-%m-%d %H:%M:%S")
        else:
            v['fecha_creacion'] = ""
    return jsonify(crops)


#Cultivo mantenimiento create-update
@main.route('/crops/crop-createupdate')
@login_required
def crop_form_page():
    idcrop = request.args.get('id', type=int)
    id_company = ObtainCompanyId()
    crop = crop_model.get_onecrop(idcrop, id_company) if idcrop else None

    return render_template(
        '/crops/create-update.html',
        use_datatables=True,
        use_visitorcss=False,
        crop=crop,
    )

@main.route('/crops/page', methods=['POST'])
@login_required
def crop_form_action():
    try:
        data = request.get_json()
        idcrop = int(data.get('idcrop', 0))
        name = data.get('name', '').strip()
        scientific_name = data.get('scientific_name', '').strip()
        description = data.get('description', '').strip()
        id_company = ObtainCompanyId()

        if not name or not scientific_name or not description:
            return jsonify({"success": False, "error": "Campos obligatorios incompletos"}), 400

        crop_obj = crop(name, scientific_name, description, id_company, idcrop if idcrop else 0)

        if idcrop:
            result = crop_model.update_crop(crop_obj)
            message = "Fundo actualizado correctamente"
        else:
            result = crop_model.save_farm(crop_obj)
            message = "Fundo creado correctamente"

        if result.get("success"):
            return jsonify({"success": True, "message": message}), 200
        return jsonify({"success": False, "error": result.get("error", "Error desconocido")}), 409

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
