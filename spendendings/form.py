from flask import Blueprint, render_template, request, abort

from spendendings.db import get_db
import re

isFloatRe = re.compile(r"\d*(\.\d+)?$")
bp = Blueprint("form", __name__, url_prefix="/project/")

@bp.route("/<id>/", methods=["GET", "POST"])
def show_form(id):
    # TODO: sanitize id
    dbEntry = get_db().execute(f"SELECT title, goal, estimated_contributors FROM project WHERE uuid = ?", [id]).fetchone()
    if dbEntry is None:
        abort(404, "This project does not exist.")
        
    if request.method == "GET": # show login
        return render_template("login.html", project={"name": dbEntry[0]})
    
    elif request.method == "POST": # show form
        thisContribution = get_db().execute(f"SELECT id, lower, upper FROM donation WHERE project_id = ? AND alias = ?", (id, request.form['alias'])).fetchone()
        # if thisContribution == None:
        #     thisContribution = {"id":}
        contributions = get_db().execute(f"SELECT lower, upper FROM donation WHERE project_id = ?", [id]).fetchall()
        return render_template("form.html", project={
            "name": dbEntry[0],
            "goal": dbEntry[1],
            "coveredMin": round(sum([elem[0] for elem in contributions]), 2),
            "coveredMax": round(sum([elem[1] for elem in contributions]), 2),
            "estDons": dbEntry[2],
            "regDons": len(contributions),
            "avgDon": round(sum([(elem[0] + elem[1]) / 2 for elem in contributions]) / len(contributions), 2) if len(contributions) != 0 else "– ",
            "startRecommendation": round(dbEntry[1] / dbEntry[2], 2),
            "liveRecommendationAvailable": dbEntry[2] - len(contributions) > 0,
            "liveRecommendationMin": round((dbEntry[1] - sum([elem[1] for elem in contributions])) / (dbEntry[2] - len(contributions)), 2) if dbEntry[2] - len(contributions) > 0 else "– ",
            "liveRecommendationMax": round((dbEntry[1] - sum([elem[0] for elem in contributions])) / (dbEntry[2] - len(contributions)), 2) if dbEntry[2] - len(contributions) > 0 else "– ",
            "minCont": "" if thisContribution is None else thisContribution['lower'],
            "maxCont": "" if thisContribution is None else thisContribution['upper'],
            "alias" : request.form['alias'],
            "submitCaption": "Add contribution" if thisContribution is None else "Update contribution",
            "deletable": not(thisContribution is None),
            "apiEndpoint": f"/project/{id}/" + ("new" if thisContribution is None else "update")
        })
        
@bp.route("/<id>/new", methods=["POST"])
def new_contribution(id):
    minV = request.form['minValue']
    maxV = request.form['maxValue']
    if re.match(isFloatRe, minV) is None:
        abort(400, f"{minV} is not a valid number.")
    if re.match(isFloatRe, maxV) is None:
        abort(400, f"{maxV} is not a valid number.")
    if float(minV) > float(maxV):
        abort(400, "Your maximal contribution must not be less than your minimal contribution.")
    
    get_db().execute("INSERT INTO donation (project_id, alias, lower, upper) VALUES (?, ?, ?, ?)", (
        id,
        request.form['alias'],
        minV,
        maxV
    ))
    get_db().commit()
    return render_template("submit.html", id=id)

@bp.route("/<id>/update", methods=["POST"])
def update_contribution(id):
    minV = request.form['minValue']
    maxV = request.form['maxValue']
    if re.match(isFloatRe, minV) is None:
        abort(400, f"{minV} is not a valid number.")
    if re.match(isFloatRe, maxV) is None:
        abort(400, f"{maxV} is not a valid number.")
    if float(minV) > float(maxV):
        abort(400, "Your maximal contribution must not be less than your minimal contribution.")
    
    get_db().execute("UPDATE donation SET lower = ?, upper = ? WHERE alias = ?", (
        minV,
        maxV,
        request.form['alias']
    ))
    get_db().commit()
    return render_template("submit.html", id=id)

@bp.route("/<id>/delete", methods=("POST",))
def delete_contribution(id):
    get_db().execute("DELETE FROM donation WHERE alias = ?", (request.form['alias'],))
    get_db().commit()
    return render_template("submit.html", id=id)