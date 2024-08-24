
from app.blueprints.login.login import *
from app.database.models import *
from app.forms.form  import *
from flask import Blueprint
import csv
from datetime import datetime, time, timedelta
#Home Page
home_bp = Blueprint('home',__name__)

@home_bp.route('/')
@login_required
def Home():
    now= datetime.today()
    queue_count = Auditing.query.count()

    current=now.strftime("%m/%d/20%y")
    date=now.strftime("%A")
    #sa= gspread.service_account(filename="Keys.json")
    #sh= sa.open("Quality Auditing Queue")
    #wks=sh.worksheet("Form Response")
    #counter= wks.get_all_records()
    count = 0



    #for i in Audited:
     #    if i['quality_agent'] == current_user.email and i['no_time']==current: 
      #      count+=1
    return render_template("Home.html",date=date,count=count,queue_count=queue_count)