from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Usename',
                           validators=[DataRequired(), Length(min=6, max=20)])
    firstname = StringField('Firstname',
                           validators=[DataRequired(), Length(min=2, max=20)])
    lastname= StringField('Laststname',
                           validators=[DataRequired(), Length(min=2, max=20)])
    gender = RadioField('Gender', choices = [('M','Male'),('F','Female')])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        user= User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken. Please choose another one.')
    def validate_email(self, email):
        user= User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already taken. Please choose another one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    firstname = StringField('Firstname',
                           validators=[DataRequired(), Length(min=2, max=20)])
    lastname= StringField('Laststname',
                           validators=[DataRequired(), Length(min=2, max=20)])
    gender = RadioField('Gender', choices = [('M','Male'),('F','Female')])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[DataRequired(), FileAllowed(['jpeg','jpg','png'])])
    submit = SubmitField('Update')
    def validate_email(self, email):
        if email.data!=current_user.email:
            user= User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is already taken. Please choose another one.')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    picture = FileField('picture', validators=[DataRequired(), FileAllowed(['jpeg','jpg','png'])])
    submit = SubmitField('Upload')
