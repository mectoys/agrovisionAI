from flask import Blueprint, jsonify, render_template, request, session

from src.models.plot_model import plot_model
from src.models.farm_model import farm_model
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


def ObtainCompanyId():
    usuario = session.get('usuario')
    if not usuario:
        return jsonify([]), 401
    id_company = usuario.get('company_id')
    return id_company


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
    idfarm = 2 #request.args.get('idfarm')
    company_id = ObtainCompanyId()
    plots = plot_model.get_plots(idfarm, company_id)

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
    plot = plot_model.get_plots(idplot) if idplot else None

    #Obtener el nombre del fundo

    idfarm = request.args.get('idfarm')
    id_company = ObtainCompanyId()
    if idfarm:
        farm = farm_model.get_onefarm(idfarm, id_company) if idfarm else None

    return render_template(
        '/plots/create-update.html',
        use_datatables=True,
        use_visitorcss=False,
        plot=plot,
        farm=farm
    )


@main.route('/plots/page', methods=['POST'])
@login_required
def plot_form_action():
    try:
        data = request.get_json()
        idplot = int(data.get('idplot', 0))

        idfarm = int(data.get('idfarm', 0))

        idcrop = int(data.get('idcrop', 0))

        name = data.get('name', '').strip()

        area = float(data.get('area', 0))
        id_company = ObtainCompanyId()
        if not name:
            return jsonify({"success": False, "error": "Campos obligatorios incompletos"}), 400

        plot_obj = plot(idfarm, idcrop, name, '01/01/206', area, id_company, idplot if idplot else 0)
        if idplot:
            result = plot_model.update_plot(plot_obj)
            message = "Parcela actualizado correctamente"
        else:
            result = plot_model.save_plot(plot_obj)
            message = "Parcela creado correctamente"

        if result.get("success"):
            return jsonify({"success": True, "message": message}), 200
        return jsonify({"success": False, "error": result.get("error", "Error desconocido")}), 409

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
