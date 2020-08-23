from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_required
from apptest import db
from apptest.models import User, ProjectData
from apptest.projects.forms import ProjDataForm

# projs = projects
projects = Blueprint("projects", __name__)


# go into the individual project details
@projects.route("/datas/<int:proj_id>")
@login_required
def proj(proj_id):
    proj = ProjectData.query.get_or_404(proj_id)
    return render_template("proj.html", title=proj.proj_title, proj=proj)


# update the project here
@projects.route("/datas/<int:proj_id>/update", methods=["GET", "POST"])
@login_required
def proj_update(proj_id):
    proj_data_form = ProjDataForm()
    proj = ProjectData.query.get(proj_id)
    if proj_data_form.validate_on_submit():
        proj.proj_title = proj_data_form.proj_title.data
        proj.aprvd_budget = proj_data_form.aprvd_budget.data
        db.session.commit()
        flash("Project has been updated!", "success")
        return redirect(url_for("projects.proj", proj_id=proj.id))
    elif request.method == "GET":
        proj_data_form.proj_key.data = proj.proj_key
        proj_data_form.proj_title.data = proj.proj_title
        proj_data_form.aprvd_budget.data = proj.aprvd_budget
    return render_template(
        "update_data.html", title=proj.proj_title, proj_data_form=proj_data_form
    )


# TODO: check decimal and try to work it out
@projects.route("/datas/new", methods=["GET", "POST"])
@login_required
def add_data():
    proj_data_form = ProjDataForm()
    # check if data is valid
    if proj_data_form.validate_on_submit():
        proj_data = ProjectData(
            proj_key=proj_data_form.proj_key.data,
            proj_title=proj_data_form.proj_title.data,
            aprvd_budget=proj_data_form.aprvd_budget.data,
        )
        # adds the project to db
        db.session.add(proj_data)
        db.session.commit()
        flash("New Project Added", category="info")
        return redirect(url_for("main.datas"))
    return render_template(
        "add_data.html", title="Add Data", proj_data_form=proj_data_form
    )


@projects.route("/datas/<int:proj_id>/delete", methods=["POST"])
@login_required
def delete_project(proj_id):
    proj = ProjectData.query.get(proj_id)
    db.session.delete(proj)
    db.session.commit()
    flash("Project has been deleted", "success")
    return redirect(url_for("main.datas"))
