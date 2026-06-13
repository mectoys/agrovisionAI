from flask import Blueprint, jsonify, render_template, request, session

from src.models.farm_model import farm_model
from src.models.entities.farm import farm
from src.utils.decorators import admin_required, login_required


main = Blueprint('bp_farm', __name__)

#Obtener datos de usuario por sesion
def ObtainUserId():
    usuario = session.get('usuario')
    if not usuario:
        return jsonify([]), 401
    id_user = usuario.get('id')
    return id_user


@main.route('/farms')
@login_required
def list_farms():

    return render_template(
        '/farms/list.html',
        use_datatables=True,
        use_visitorcss=False,
    )
#Cargar listado de Fincas Farms
@main.route('/farms/data')
@login_required
def Farms_data():
    id_user = ObtainUserId()
    farms = farm_model.get_farms(id_user)

    for v in farms:
        # Formateo fecha creacion
        if v['fecha_creacion']:
            v['fecha_creacion'] = v['fecha_creacion'].strftime("%Y-%m-%d %H:%M:%S")
        else:
            v['fecha_creacion'] = ""
    return jsonify(farms)


#Fundo mantenimiento create-update
@main.route('/farms/farm-createupdate')
@login_required
def farm_form_page():
    idfarm = request.args.get('id', type=int)
    farm = farm_model.get_onefarm(idfarm) if idfarm else None
    return render_template(
        '/farms/create-update.html',
        use_datatables=True,
        use_visitorcss=False,
        farm=farm,
    )


@main.route('/farms/page', methods=['POST'])
@login_required
def farm_form_action():
    try:
        data = request.get_json()
        idfarm = int(data.get('idfarm', 0))
        name = data.get('name', '').strip()
        location = data.get('location', '').strip()
        area_hectares = float(data.get('area_hectares', 0))
        id_user = ObtainUserId()

        if not name or not location or not area_hectares:
            return jsonify({"success": False, "error": "Campos obligatorios incompletos"}), 400

        farm_obj = farm(id_user, name, location, area_hectares, idfarm if idfarm else 0)
        if idfarm:
            result = farm_model.update_farm(farm_obj)
            message = "Fundo actualizado correctamente"
        else:
            result = farm_model.save_farm(farm_obj)
            message = "Fundo creado correctamente"

        if result.get("success"):
            return jsonify({"success": True, "message": message}), 200
        return jsonify({"success": False, "error": result.get("error", "Error desconocido")}), 409

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
