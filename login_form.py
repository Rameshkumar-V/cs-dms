from flask_wtf import FlaskForm
from wtforms import StringField,DateTimeField,SelectField,PasswordField,BooleanField,TextAreaField,SubmitField,DateField
from wtforms.validators import DataRequired,Length



class MyForm(FlaskForm):
    roll_no = StringField('Enter Rollno', validators=[DataRequired(),Length(min=5,max=20)])
    dob = DateField('Enter DOB', format='%Y-%m-%d',validators=[DataRequired()])
    category = SelectField("Select Year",validators=[DataRequired()], choices=[],validate_choice=False)
    submit = SubmitField("Submit")


class AdminForm(FlaskForm):
    username = StringField('Enter Username', validators=[DataRequired(),Length(min=5,max=20)])
    password = PasswordField("Enter Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class DiscussionForm(FlaskForm):
    vote = SelectField("Accept or De-Accept",validators=[DataRequired()], choices=[(1,"Accept"),(0,"No")])
    remarks = TextAreaField("Enter Your Remarks here",validators=[Length(max=2000)])
    submit = SubmitField("Submit")
