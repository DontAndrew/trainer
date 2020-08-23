from datetime import datetime
from apptest import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def login_manager(user_id):
    return User.query.get(int(user_id))


# creating user for the app
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}','{self.image_file}', '{self.password})"


# dummy class delete this later
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


# creating new project
class ProjectData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    proj_key = db.Column(db.String(20), unique=True, nullable=False)
    proj_title = db.Column(db.String(180), unique=False, nullable=False)
    aprvd_budget = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f"Project('{self.proj_key}', '{self.proj_title}', '{self.aprvd_budget}')"
