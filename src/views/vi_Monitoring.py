from flask import Blueprint, jsonify, render_template, request, session

from src.utils.decorators import admin_required, login_required

main = Blueprint('bp_monitoring', __name__)

@main.route('/monitoring/new-analysis')
@login_required
def nuevo_analisis():
    return render_template(
        '/monitoring/new_analysis.html',
        use_datatables=False,
        use_visitorcss=False,
    )
