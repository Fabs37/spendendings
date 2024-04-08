from flask import (
    Blueprint, render_template, current_app
)

from spendendings.db import get_db

bp = Blueprint('projectlist', __name__, url_prefix='/')

@bp.route("/", methods=["GET", "POST"])
def list_projects():
    return render_template("projectlist.html", projects=[{"id": elem[0], "name": elem[1]} for elem in get_db().execute("SELECT uuid, title FROM project").fetchall()], show=current_app.config['SHOW_PROJECT_INDEX'])
