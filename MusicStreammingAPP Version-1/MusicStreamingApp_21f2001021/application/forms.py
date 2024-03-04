from flask_wtf import FlaskForm
from wtforms import PasswordField,SubmitField,FileField,StringField , ValidationError , SelectMultipleField
from wtforms.validators import DataRequired ,Length,Email
from application.data.models import *
import re

class RegistrationForm(FlaskForm):
    name=StringField(label='Name', validators=[DataRequired()] )
    email_id=StringField(label="Email_id",validators=[DataRequired(), Email()]) 
    password=PasswordField(label="Password",validators=[DataRequired(), Length(min=8)])
    submit=SubmitField()
    
    def validate_name(self,field):
        names=field.data
        if not names.isalpha():
            raise ValidationError('Name should contains alphabhets only')
    def validate_email_id(self,field):
        if field.data != self.original_email:
            names=field.data
            existing_email= User.query.filter_by(email_id=names).first()
            if existing_email:
                raise ValidationError('Email_id  already exists.')
    # def validate_password(self, field):
    #     password = field.data
    #     regex= r'^(?=.*[!@#$%^&*()_+=\-;:/|\\?.,<>~])(?=.*[A-Z])(?=.*[a-z])(?=.*\d){8,}$'
    #     if not re.match(regex,password):
    #         raise ValidationError('Password Should contain atleast one special character, one upper case letter , one lower case letter , one digit ')
            
    def __init__(self, submit_name='Register', original_email=None,*args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.submit.label.text = submit_name
        self.original_email = original_email

class LoginForm(FlaskForm):
    email_id=StringField(label="Email_id",validators=[DataRequired(),Email()])
    password=PasswordField(label="Password",validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(label='Login')
    
    
class Upload_Song(FlaskForm):
    song_title=StringField(label="Song_Title",validators=[DataRequired()])
    release_date=StringField(label="Release_date",validators=[DataRequired()])
    genre=StringField(label="Genre", validators=[DataRequired()])
    language=StringField(label="Language", validators=[DataRequired()])
    lyrics = StringField(label="Lyrics", validators=[DataRequired()])
    song_file =FileField(label="Upload Song",validators=[DataRequired()])
    song_pic=FileField(label="Song_pic")
    submit = SubmitField()
    def __init__(self, submit_name='Upload',*args, **kwargs):
        super(Upload_Song, self).__init__(*args, **kwargs)
        self.submit.label.text= submit_name
    def validate_song_title(self,field):
        
        names = field.data
        existing_song= Songs.query.filter_by(song_title=names).first()
        if existing_song:
            raise ValidationError('Song title already exists.')     
class PlaylistForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    songs = SelectMultipleField('Songs', coerce=int)
    submit = SubmitField('Submit')
