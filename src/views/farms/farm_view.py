from flask import Blueprint, jsonify, render_template, request, session

from src.models.farm_model import farm_model
from src.models.entities.farm import farm
from src.utils.decorators import admin_required, login_required


main = Blueprint('bp_farm', __name__)


@main.route('/farms')
@admin_required
def list_farms():
    farms = farm_model.get_farms()
    print("data")
    return render_template(
        '/farms/list.html',
        farms=farms,
        use_datatables=True,
        use_visitorcss=False,
    )
#Cargar listado de Fincas Farms
@main.route('/farms/data')
@admin_required
def Farms_data():
    farms = farm_model.get_farms()
    for v in farms:
        # Formateo fecha creacion
        if v['fecha_creacion']:
            v['fecha_creacion'] = v['fecha_creacion'].strftime("%Y-%m-%d %H:%M:%S")
        else:
            v['fecha_creacion'] = ""
    return jsonify(farms)


#Fundo mantenimiento create-update
@main.route('/farms/farm-createupdate')
@admin_required
def usuario_form_page():
    idfarm = request.args.get('id', type=int)
    usuario = Farms_data.get_onefarm(idfarm) if idfarm else None
    return render_template(
        '/farms/create-update.html',
        use_datatables=True,
        use_visitorcss=False,
        farm=farm,
    )
