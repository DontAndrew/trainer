from flask import Blueprint, render_template, url_for, flash, redirect
from flask_login import current_user, logout_user, login_user, login_required
from apptest.users.forms import LoginForm, RegistrationForm
from apptest import db, bcrypt
from apptest.models import User

users = Blueprint("users", __name__)


@users.route("/", methods=["GET", "POST"])
@users.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    # lets you stay login
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    # check if login data is valid
    if login_form.validate_on_submit():
        # checking if email is in db
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user)
            flash("Login Successfully", category="info")
            return redirect(url_for("main.dashboard"))
        else:
            flash("Login Unsuccessful", category="danger")
    return render_template("login.html", title="Login", login_form=login_form)


@users.route("/register", methods=["GET", "POST"])
@login_required
def register():
    register_form = RegistrationForm()

    # check if register data is valid
    if register_form.validate_on_submit():
        # creating hashed password
        hashed_password = bcrypt.generate_password_hash(
            register_form.password.data
        ).decode("utf - 8")
        # creating a user with hashed password
        user = User(
            username=register_form.username.data,
            email=register_form.email.data,
            password=hashed_password,
        )
        # adds the 'user' to the db
        db.session.add(user)
        db.session.commit()

        flash("Account successfully created", category="success")
        return redirect(url_for("users.login"))
    return render_template(
        "register.html", title="register", register_form=register_form
    )


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("users.login"))

