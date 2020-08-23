from flask import Blueprint, render_template
from flask_login import login_required
from apptest.models import ProjectData

main = Blueprint("main", __name__)


@main.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", title="Dashboard")


@main.route("/datas")
@login_required
def datas():
    datas = ProjectData.query.all()
    return render_template("datas.html", title="Datas", datas=datas)


@main.route("/about")
@login_required
def about():
    return render_template("about.html", title="About")  # TODO: create an about page

