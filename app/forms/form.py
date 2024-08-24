import csv
from datetime import datetime, time, timedelta
from flask import Flask,render_template, url_for,redirect,flash,request, jsonify, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField,PasswordField,DateField,FileField,RadioField,DateTimeField,HiddenField,EmailField,TextAreaField,IntegerField
from wtforms.validators import DataRequired
from flask_login import UserMixin, login_user,LoginManager,login_required,logout_user,current_user
from app.database.db_connection import dbconnection,engine
from app.secretcode import secret_code


class QualityForm(FlaskForm):
    cx_agent=StringField("CX Agent",validators=[DataRequired()])
    supervisor=StringField("Supervisor",validators=[DataRequired()])
    convo_link=StringField("Convo Link",validators=[DataRequired()])
    date_of_conversation=DateField("Date Of Conversation",validators=[DataRequired()])
    quality_agent=StringField("Quality Agent")
    label=StringField("Label",validators=[DataRequired()])
    assigned_group=StringField('Assigned_Group',validators=[DataRequired()])
    assigned_date=HiddenField('Assigned Date')
   # timestamp = DateTimeField("Timestamp", default=datetime.utcnow, validators=[DataRequired()])
    #name = StringField("Name", default=get_default)  
    submit= SubmitField()
#Add UserForm
class UserForm(FlaskForm):
    first_name=StringField("First Name",validators=[DataRequired()])
    second_name=StringField("Second Name",validators=[DataRequired()])
    email=StringField("Email",validators=[DataRequired()])
    password=PasswordField("Password",validators=[DataRequired()])
    role= StringField("role",validators=[DataRequired()])
    submit= SubmitField()
#Login Form
class LoginForm(FlaskForm):
    email= EmailField("Email",validators=[DataRequired()])
    password=PasswordField("Password",validators=[DataRequired()])
    submit= SubmitField()
#add chats Form
class AuditForm(FlaskForm):
    time_stamp=DateTimeField("Time Stamp")
    cx_agent=StringField("CX Agent",validators=[DataRequired()])
    supervisor=StringField("Supervisor",validators=[DataRequired()])
    convo_link=StringField("Convo Link",validators=[DataRequired()])
    date_of_conversation=StringField("Date Of Conversation",validators=[DataRequired()])
    quality_agent=StringField("Quality Agent")
    label=StringField("Label",validators=[DataRequired()])
    assigned_group=StringField('Assigned_Group',validators=[DataRequired()])
    assigned_date=StringField('Assigned Date')
    date= DateField('Date')

    Active_Listining=RadioField('Active Listening',validators=[DataRequired()],choices=[('Zero Pointed','Zero Pointed'),('Full Pointed','Full Pointed')])
    Active_Listining_comment=StringField('Comment')
    Identification_of_contact=RadioField('Identification of contact reason & Problem',validators=[DataRequired()],choices=[('Zero Pointed','Zero Pointed'),('Full Pointed','Full Pointed')])
    Identification_of_contact_comment=StringField('Comment')
    Information_Accuracy=RadioField('Information Accuracy',validators=[DataRequired()],choices=[('Zero Pointed','Zero Pointed'),('Full Pointed','Full Pointed')])
    Information_Accuracy_comment=StringField('Comment')
    Proactively_providing_solution=RadioField('Proactively providing feedback and the best solution',validators=[DataRequired()],choices=[('Zero Pointed','Zero Pointed'),('Full Pointed','Full Pointed')])
    Proactively_providing_solution_comment=StringField('Comment')    
    Format_Writing_Professionalism=RadioField('Format, Writing, & Professionalism',validators=[DataRequired()],choices=[('Zero Pointed','Zero Pointed'),('Full Pointed','Full Pointed')])
    Format_Writing_Professionalism_comment=StringField('Comment')
    Documented_notes_information=RadioField('Documented notes & case information',validators=[DataRequired()],choices=[('Zero Pointed','Zero Pointed'),('Full Pointed','Full Pointed')])
    Documented_notes_information_comment=StringField('Comment')
    Ticket_escalation=RadioField('Ticket escalation',validators=[DataRequired()],choices=[('Zero Pointed','Zero Pointed'),('Full Pointed','Full Pointed')])
    Ticket_escalation_comment=StringField('Comment')
    Setting_correct_Follow_up=RadioField('Ticket escalation',validators=[DataRequired()],choices=[('Zero Pointed','Zero Pointed'),('Full Pointed','Full Pointed')])
    Setting_correct_Follow_up_comment=StringField('Comment')
    Contact_reason=RadioField('Ticket escalation',validators=[DataRequired()],choices=[('Zero Pointed','Zero Pointed'),('Full Pointed','Full Pointed')])
    Contact_reason_comment=StringField('Comment')
    Adherence_to_procedures=RadioField('Adherence to policies and procedures',validators=[DataRequired()],choices=[('Zero Pointed','Zero Pointed'),('Full Pointed','Full Pointed')])
    Adherence_to_procedures_comment=StringField('Comment')
    Opening_Closing=RadioField('Opening & Closing',validators=[DataRequired()],choices=[('Zero Pointed','Zero Pointed'),('Full Pointed','Full Pointed')])
    Opening_Closing_comment=StringField('Comment')
    Apologizing_Empathy=RadioField('Apologizing & Empathy',validators=[DataRequired()],choices=[('Zero Pointed','Zero Pointed'),('Full Pointed','Full Pointed')])
    Apologizing_Empathy_comment=StringField('Comment')              
    Active_Acknowledgment=RadioField('Active Listening/ Reply & Acknowledgment',validators=[DataRequired()],choices=[('Zero Pointed','Zero Pointed'),('Full Pointed','Full Pointed')])
    Active_Acknowledgment_comment=StringField('Comment')              
    Conversation_Control=RadioField('Conversation Control',validators=[DataRequired()],choices=[('Zero Pointed','Zero Pointed'),('Full Pointed','Full Pointed')])
    Conversation_Control_comment=StringField('Comment')
    Confidentiality=RadioField('Confidentiality',validators=[DataRequired()],choices=[('Zero Pointed','Zero Pointed'),('Full Pointed','Full Pointed')])
    Confidentiality_comment=StringField('Comment')    
    auto_fail=RadioField('Is Contact Auto-fail?',validators=[DataRequired()],choices=[('Yes','Yes'),('No','No')])
    observation_recommendation=TextAreaField('Observation / Recommendations')
    auditing_id=IntegerField('auditing_id',validators=[DataRequired()])
    #csv_upload=FileField("Upload CSV File",validators=[DataRequired()])
    submit_button_1 = SubmitField('Submit & Next')
    submit_button_2 = SubmitField('Submit & Exit')
    submit_button_3 = SubmitField('Skip')
    submit_button_4 = SubmitField('Update')

class FilterForm(FlaskForm):
    
    start_date=DateField('Start Date')
    end_date=DateField('End Date')
    submit=SubmitField('Submit')