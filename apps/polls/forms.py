from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.validators import NumberRange


class ProfileForm(FlaskForm):
    user_gender = StringField('User Gender: ')
    user_age = IntegerField('User Age: ')


class EvaluationForm(FlaskForm):
    happy_rate = IntegerField('Your happy rate: ', validators=[NumberRange(min=1, max=5)])
    mood_rate = IntegerField('Your mood rate: ', validators=[NumberRange(min=1, max=5)])
    description = TextAreaField('Your description: ')
