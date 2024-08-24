import csv
from datetime import datetime, time, timedelta
from flask import Flask,render_template, url_for,redirect,flash,request, jsonify, send_from_directory,blueprints
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField,PasswordField,DateField,FileField,RadioField,DateTimeField,HiddenField,EmailField,TextAreaField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,sessionmaker,session,Session,scoped_session, sessionmaker, declarative_base
from sqlalchemy import Integer, String, DateTime,Date,Time,TIMESTAMP,BINARY,insert,create_engine,all_,Delete,column,ForeignKey,Boolean
from werkzeug.security import generate_password_hash,check_password_hash
from flask_migrate import Migrate
from flask_login import UserMixin, login_user,LoginManager,login_required,logout_user,current_user
from app.database.db_connection import dbconnection,engine
from app.secretcode import secret_code
import pytz
import gspread
import psycopg2
import os
import json
from app.forms.form import *
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
# models_bp = blueprints('models',__name__)
from flask_login import UserMixin

Base = declarative_base()

#Initialize Database
db=SQLAlchemy(model_class=Base)

#users database

class Users(Base,UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)


    def set_password(self,password):
        self.password =generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)
    
    @classmethod
    def get_user_by_email(cls,email):
        return db.session.query(cls).filter_by(email=email).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Auditing(Base):
    __tablename__ = 'auditing'

    id = Column(Integer, primary_key=True)
    cx_agent = Column(String, nullable=False)
    supervisor = Column(String, nullable=False)
    convo_link = Column(String, nullable=False)
    quality_agent = Column(String, nullable=True)
    label = Column(String, nullable=False)
    assigned_group = Column(String, nullable=False)
    assigned_date = Column(DateTime, nullable=True)
    date_of_conversation = Column(String, nullable=False)
    skip=Column(Boolean,nullable=True,default=False)

    
    
class Audited(Base):
    __tablename__ = 'audited'

    id = Column(Integer, primary_key=True)
    auditing_id = Column(Integer)
    date = Column(Date, nullable=True)
    cx_agent = Column(String, nullable=False)
    supervisor = Column(String, nullable=False)
    convo_link = Column(String, nullable=False)
    quality_agent = Column(String, nullable=True)
    label = Column(String, nullable=False)
    assigned_group = Column(String, nullable=False)
    assigned_date = Column(String, nullable=True)
    date_of_conversation = Column(String, nullable=False)
    time_stamp = Column(String, nullable=True)
    Active_Listining = Column(String, nullable=True)
    Active_Listining_comment = Column(String, nullable=True)
    Identification_of_contact = Column(String, nullable=True)
    Identification_of_contact_comment = Column(String, nullable=True)
    Information_Accuracy = Column(String, nullable=True)
    Information_Accuracy_comment = Column(String, nullable=True)
    Proactively_providing_solution = Column(String, nullable=True)
    Proactively_providing_solution_comment = Column(String, nullable=True)
    Format_Writing_Professionalism = Column(String, nullable=True)
    Format_Writing_Professionalism_comment = Column(String, nullable=True)
    Documented_notes_information = Column(String, nullable=True)
    Documented_notes_information_comment = Column(String, nullable=True)
    Ticket_escalation = Column(String, nullable=True)
    Ticket_escalation_comment = Column(String, nullable=True)
    Adherence_to_procedures = Column(String, nullable=True)
    Adherence_to_procedures_comment = Column(String, nullable=True)
    Opening_Closing = Column(String, nullable=True)
    Opening_Closing_comment = Column(String, nullable=True)
    Apologizing_Empathy = Column(String, nullable=True)
    Apologizing_Empathy_comment = Column(String, nullable=True)
    Setting_correct_Follow_up = Column(String, nullable=True)
    Setting_correct_Follow_up_comment = Column(String, nullable=True)
    Contact_reason = Column(String, nullable=True)
    Contact_reason_comment = Column(String, nullable=True)
    Active_Acknowledgment = Column(String, nullable=True)
    Active_Acknowledgment_comment = Column(String, nullable=True)
    Conversation_Control = Column(String, nullable=True)
    Conversation_Control_comment = Column(String, nullable=True)
    Confidentiality = Column(String, nullable=True)
    Confidentiality_comment = Column(String, nullable=True)
    auto_fail = Column(String, nullable=True)
    # Total_score= Column(Integer,nullable=True)
    observation_recommendation = Column(String, nullable=True)

# class Attributes(Base):
#     __tablename__='attributes'

#     id=Column(Integer, primary_key=True)
#     attribute= Column(String,nullable=False)
#     weight=Column(Integer,nullable=False)
#     auto_fail=Column(Boolean,nullable=False)

