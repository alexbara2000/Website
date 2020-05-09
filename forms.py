from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, RadioField
from wtforms.validators import InputRequired, Regexp, EqualTo


class QuizForm(FlaskForm):
    question1 = RadioField('Where was I born?', validators=[InputRequired()],
                           choices=[('r1', 'Canada'), ('r2', 'USA'), ('r3', 'Roumania'), ('r4', 'France')],
                           render_kw={'required': True})
    question2 = RadioField('What is my dad name?', validators=[InputRequired()],
                           choices=[('r1', 'Valentin'), ('r2', 'Adrian'), ('r3', 'Sorin'), ('r4', 'John')],
                           render_kw={'required': True})
    question3 = RadioField('What high school did I attend?', validators=[InputRequired()],
                           choices=[('r1', 'Sainte-Louis'), ('r2', 'CSA'), ('r3', 'WIC'), ('r4', 'School?')],
                           render_kw={'required': True})
    question4 = RadioField('What University am I going to?', validators=[InputRequired()],
                           choices=[('r1', 'Mcgill'), ('r2', 'UQAM'), ('r3', 'Concordia'), ('r4', 'UDM')],
                           render_kw={'required': True})
    question5 = RadioField('What is my favorite passtime?', validators=[InputRequired()],
                           choices=[('r1', 'Video games'), ('r2', 'Reading'), ('r3', 'Eating'), ('r4', 'Gym')],
                           render_kw={'required': True})


class SignUpForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password', validators=[InputRequired(), Regexp('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,20}$', 0,
                                                                 'Password is not in valid form, The password must contain '
                                                                 ' at least one upper and lower case letter, at least one digit,'
                                                                 ' the length is between 8 and 20 and it has no spaces.')])
    password2 = PasswordField('Repeat password',
                              validators=[InputRequired(), EqualTo('password', message='passwords must be the same')])
    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password',
                             validators=[InputRequired()])
    submit = SubmitField('Login')


class ForgotPassword(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password',validators=[InputRequired(), Regexp('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,20}$', 0,
                                                                 'Password is not in valid form, The password must contain '
                                                                 ' at least one upper and lower case letter, at least one digit,'
                                                                 ' the length is between 8 and 20 and it has no spaces.')])
    password2 = PasswordField('Repeat password',
                              validators=[InputRequired(), EqualTo('password', message='passwords must be the same')])
    submit = SubmitField('Reset password')


