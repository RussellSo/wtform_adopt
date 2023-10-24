from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import InputRequired, Optional, URL

species = ['cat', 'dog', 'porcupine']

class AddPetForm(FlaskForm):
    name = StringField("Pet Name", validators=[InputRequired()])
    species = SelectField("Species", choices=[(sp,sp )for sp in species], render_kw={"placeholder": "n/a"})
    photo_url = StringField('Photo', validators=[Optional(), URL()])
    age = IntegerField('Age')
    notes = StringField('notes')
