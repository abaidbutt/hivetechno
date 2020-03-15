from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, RadioField, SelectField, TextAreaField, BooleanField, DecimalField, PasswordField,DateTimeField
from wtforms.validators import DataRequired, Email, NumberRange, Length, EqualTo, ValidationError, InputRequired, Optional
from wtforms_validators import Alpha, Integer
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.widgets import html5
import datetime
from hive import db
from hive.models import Courses, User

from flask_login import current_user
# _values=[]
# _choices = []
# courses=Courses.query.filter_by(course_status=True).all()
# for course in courses:
#     _value=[]
#     _choice=[]
#     _choice.append(str(course.id))
#     _value.append(str(course.id))
#     _choice.append(course.course_name)
#     _value.append(str(course.course_fee))
    
#     _choice=tuple(_choice)
#     _value=tuple(_value)

#     _choices.append(_choice)
#     _values.append(_value)

class RegisterForm(FlaskForm):
    user_name = StringField('Name', validators=[DataRequired(), Alpha()])
    father_name = StringField('Father Name', validators=[DataRequired(), Alpha()])
    dob = DateField('Date of Birth', format='%Y-%m-%d')
    cnic=IntegerField('CNIC', widget=html5.NumberInput(), validators=[DataRequired()])
    gender = SelectField('Gender', choices = [('M','Male'),('F','Female'), ('O', 'Other')])
    admit_date=DateField('Current Date', validators=[Optional()])
    course_name=SelectField('Course Name', choices = [])
    # course_fee=SelectField('Course Fee', choices = _values)
    course_fee=SelectField('Course Fee', choices=[], validators=[Optional()])
    course_installments=SelectField('Course Installments', choices = [('1', 'one'), ('2', 'two'), ('3', 'three')])
    course_promo = StringField('Promo Code')
    course_discount = StringField('Discount', validators=[Optional()])
    total_fee = StringField('Total Fee', validators=[Optional()])
    # contact details
    personal_no=IntegerField('Personal Phone No:', widget=html5.NumberInput(), validators=[DataRequired()])
    parent_no=IntegerField('Parent Phone No:', widget=html5.NumberInput(), validators=[DataRequired()])
    email=StringField('Email', validators=[DataRequired(), Email()])
    address=TextAreaField('Address')
    # academic details
    degree=SelectField('Recent Degree', choices = [('matric', 'Matric'),('inter', 'Intermediate'),  ('dae', 'DAE'),('graduation', 'Graduation'), ('master', 'Master')])
    semester=SelectField('Semester/Part',  choices = [ ('comp', 'Completed'),('one', '1st'), ('two', '2nd')])
    institute=StringField('Institute Name', validators=[DataRequired()])
    marks=DecimalField('Marks/CGPA', validators=[DataRequired()], widget=html5.NumberInput())
    start_year=StringField('Start Year', validators=[DataRequired(), Integer()])
    end_year=StringField('End Year', validators=[DataRequired(), Integer()])
    profile_picture=FileField('Profile Picture', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'])])
    cnic_front=FileField('CNIC Front', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'])])
    cnic_back=FileField('CNIC Back', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'])])
    submit=SubmitField('Register')
    def validate_email(self, email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered. please choose different one')
    def validate_cnic(self, cnic):
        user=User.query.filter_by(c_nic=cnic.data).first()
        if len(str(cnic.data))!=13:
            raise ValidationError('cnic must be 13 digits with no dash')
        if user:
            raise ValidationError('This cnic is already registered. please choose different one')
    def validate_start_year(self, start_year):
        if len(str(start_year.data))!=4:
            raise ValidationError('start year must be 4 digits')
    def validate_end_year(self, end_year):
        if len(str(end_year.data))!=4:
            raise ValidationError('end year must be 4 digits')
    
    def validate_personal_no(self, personal_no):
        if len(str(personal_no.data))<10 or len(str(personal_no.data))>11:
            raise ValidationError('personal phone No must be 11 digits with no dash')
    def validate_parent_no(self, parent_no):
        if len(str(parent_no.data))<10 or len(str(parent_no.data))>11:
            raise ValidationError('parent phone No must be 11 digits with no dash')

class CheckForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired(), Length(min=3)])
    email = StringField('Gmail', validators=[InputRequired(), Email(), Length(min=3)])
    year=IntegerField('Start', widget=html5.NumberInput(), validators=[DataRequired()])
    profile_picture=FileField('Profile Picture', validators=[FileRequired(), FileAllowed(['jpg', 'png'])])
    submit_u=SubmitField('Update Course')
    def validate_year(self, year):
        if len(str(year.data))!=4:
            raise ValidationError('year must be 4 digits')

def choice_query():
    return User.query


class FeeSubmitForm(FlaskForm):
    rollNo=SelectField('Roll No#', choices=[], coerce=int, validators=[DataRequired()])
    enrollments=SelectField('Enrollments', choices=[], coerce=int, validators=[DataRequired()])
    total_fee=StringField('Total Fees', validators=[Optional()])
    paid_fee=StringField('Paid Fees', validators=[Optional()])
    total_installments=StringField('Total Installmenets', validators=[Optional()])
    paid_installments=StringField('Paid Installments', validators=[Optional()])
    perinsta=StringField('PerInstallments Fee', widget=html5.NumberInput(), validators=[DataRequired()])
    submit=SubmitField('Pay')
    
    def validate_perinsta(self, perinsta):
        if int(self.total_installments.data)-int(self.paid_installments.data) ==1:
            if float(self.total_fee.data)-float(self.paid_fee.data) != float(self.perinsta.data):
                raise ValidationError('This is last installment so you pay all fee')




    
    
class LoginForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired()])
    password=PasswordField('Password', validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Login')

class PasswordForm(FlaskForm):
    old_password=PasswordField('Old Password', validators=[DataRequired()])
    new_password=PasswordField('New Password', validators=[DataRequired()])
    reenter_password=PasswordField('Re-Enter Password', validators=[DataRequired(), EqualTo('new_password')])
    submit=SubmitField('Update Password')
    def validate_old_password(self, old_password):
        if old_password.data != User.query.filter_by(id=current_user.id).first().password:
            raise ValidationError('Please check your password and try another')

class EnrollmentForm(FlaskForm):
    course_name=SelectField('Course Name', choices = [], coerce=int, validators=[DataRequired()])
    # course_fee=SelectField('Course Fee', choices = _values)
    course_fee=SelectField('Course Fee', choices=[], validators=[Optional()], coerce=int)
    course_installments=SelectField('Course Installments', choices = [('1', 'one'), ('2', 'two'), ('3', 'three')])
    course_promo = StringField('Promo Code')
    course_discount = StringField('Discount', validators=[Optional()])
    total_fee = StringField('Total Fee', validators=[Optional()])
    submit=SubmitField('Enroll in Course')

    
    # def validate_username(self, username):
    #     user=User.query.filter_by(roll_no=username.data).first()
        # if username.data != 'admin@blog.com' and not(user):
    #         raise ValidationError('Please check your username ')
        
    # def validate_password(self, password):
    #     if self.username.data=='admin@blog.com':
    #         if self.password.data != 'admin':
    #             raise ValidationError('Please check your password')
    #     else:
    #         user=User.query.filter_by(roll_no=self.username.data, password=self.password.data).first()
    #         if not(user):
    #             raise ValidationError('Please check your password and username')

            


