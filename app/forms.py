from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired


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
    submit = SubmitField('Send')


class SettingsForm(FlaskForm):
    name = StringField('Название аккаунта', validators=[DataRequired()])
    oauth = PasswordField('Ouath')
    folderid = StringField('Folder ID', validators=[DataRequired()])
    submit = SubmitField('Отправить')

