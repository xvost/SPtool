from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, DecimalField
from wtforms.validators import DataRequired, NumberRange


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class SttForm(FlaskForm):
    pathtofile = StringField('File path', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class TtsForm(FlaskForm):
    text = TextAreaField('Text', validators=[DataRequired()])
    account = SelectField('KeyId', validators=[DataRequired()])
    voice = SelectField('Voice', validators=[DataRequired()])
    speed = DecimalField('Speed, from 0.1 to 3', validators=
    [NumberRange(min=0.1, max=3)], default=1)
    submit = SubmitField('Send')


class SettingsForm(FlaskForm):
    name = StringField('Название аккаунта', validators=[DataRequired()])
    oauth = PasswordField('Ouath')
    folderid = StringField('Folder ID', validators=[DataRequired()])
    submit = SubmitField('Отправить')

