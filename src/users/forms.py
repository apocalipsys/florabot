from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired, EqualTo
from src.models import Users

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Ingresar')

    def check_user(self,name):
        return True if Users.query.filter_by(username=name).first() else False


class RegisterForm(FlaskForm):
    username = StringField('Nombre de usuario: ',validators=[DataRequired()])
    password = PasswordField('Password: ',validators=[DataRequired(),EqualTo('password_confirm')])
    password_confirm = PasswordField('Confirmar password',validators=[DataRequired()])
    submit = SubmitField('Registrarlo')


    def check_user(self,name):
        return True if Users.query.filter_by(username=name).first() else False

class CambiarPassForm(FlaskForm):
    old_password = PasswordField('Password viejo: ',validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired(), EqualTo('password_confirm')])
    password_confirm = PasswordField('Confirmar password', validators=[DataRequired()])
    submit = SubmitField('Cambiar password')

    def check_user(self,name):
        return True if Users.query.filter_by(username=name).first() else False


