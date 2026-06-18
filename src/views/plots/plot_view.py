from flask import Blueprint, jsonify, render_template, request, session

from src.models.plot_model import    plot_model
from src.models.entities.plot import plot
from src.utils.decorators import admin_required, login_required


main = Blueprint('bp_plot', __name__)

#Obtener datos de usuario por sesion
def ObtainUserId():
    usuario = session.get('usuario')
    if not usuario:
        return jsonify([]), 401
    id_user = usuario.get('id')
    return id_user


@main.route('/plots')
@login_required
def list_plots():

    return render_template(
        '/plots/list.html',
        use_datatables=True,
        use_visitorcss=False,
    )
#Cargar listado de Fincas Farms
@main.route('/plots/data')
@login_required
def Plots_data():
    id_user = ObtainUserId()
    plots = plot_model.get_plots(id_user)

    for v in plots:
        # Formateo fecha creacion
        if v['fecha_creacion']:
            v['fecha_creacion'] = v['fecha_creacion'].strftime("%Y-%m-%d %H:%M:%S")
        else:
            v['fecha_creacion'] = ""
    return jsonify(plots)


#Fundo mantenimiento create-update
@main.route('/plots/plot-createupdate')
@login_required
def plot_form_page():
    idplot = request.args.get('id', type=int)
    plot = plot_model.get_onecrop(idfarm) if idfarm else None
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
