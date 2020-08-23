from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField
from wtforms.validators import DataRequired, InputRequired, ValidationError
from apptest.models import ProjectData


# creating a new PROJECT DATA
class ProjDataForm(FlaskForm):
    proj_key = StringField("Project Key", validators=[DataRequired()])
    proj_title = StringField("Project Title", validators=[DataRequired()])
    aprvd_budget = DecimalField(
        "Approved Budget for the Contract", validators=[InputRequired()], places=2,
    )
    submit = SubmitField("Submit")
    # validate if the proj key exist
    

    def validate_proj_key(self, proj_key):
        proj_key = ProjectData.query.filter_by(proj_key=proj_key.data).first()
        if proj_key:
            raise ValidationError("That Project Key already exists.")
