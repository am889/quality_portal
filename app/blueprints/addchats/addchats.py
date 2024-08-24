from flask import Blueprint,request
from app.forms.form import *
from app.database.models import *
from queue_handling.classes import Add_chats
from flask_jwt_extended import jwt_required
import gspread
import os
import json
# from flask_jwt import jwt_required


addchats_bp = Blueprint('addchats',__name__)


@addchats_bp.route('/addchats',methods=['GET','POST'])
@login_required
def add_chats():
    if current_user.role=="Admin":
        queue_count = Auditing.query.count()
        form=QualityForm()
        cx_agent=None
        supervisor=None
        convo_link=None
        quality_agent=None
        date_of_conversation=None
        assigned_group=None
        label=None
        our_chats= Auditing.query.order_by(Auditing.id)

        if form.validate_on_submit():
            our_chats=Auditing.query.filter_by(convo_link=form.convo_link.data).first()

            if our_chats is None:
                our_chats=Auditing(cx_agent=form.cx_agent.data,supervisor=form.supervisor.data,convo_link=form.convo_link.data,date_of_conversation=form.date_of_conversation.data,quality_agent=form.quality_agent.data,label=form.label.data,assigned_group=form.assigned_group.data)
                db.session.add(our_chats)
                db.session.commit()

        
            quality_agent=form.quality_agent.data
            cx_agent=form.cx_agent.data
            label=form.label.data
            assigned_group=form.assigned_group.data
            supervisor=form.supervisor.data
            convo_link=form.convo_link.data
            date_of_conversation=form.date_of_conversation.data
            form.date_of_conversation.data=''
            form.supervisor.data=''
            form.cx_agent.data=''
            form.convo_link.data=''
            form.quality_agent.data=''
            form.assigned_group.data=''
            form.label.data=''
            flash('Chats Added successfully!')

            our_chats= Auditing.query.order_by(Auditing.id)
    elif current_user.role=='User':
        return redirect(url_for('admin.adminaccess'))        
    return render_template("auditing.html",form=form,queue_count=queue_count,quality_agent=quality_agent,cx_agent=cx_agent,supervisor=supervisor,convo_link=convo_link,date_of_conversation=date_of_conversation,ourchats=our_chats,assigned_group=assigned_group,label=label)   


@addchats_bp.post('/addchatsapi')
@jwt_required()
def add_income():
    Add_chats.read_api(request.get_json())
    Add_chats.move_chats_to_db(table=Auditing,db=db)
    Add_chats.all_chats.clear()
    return jsonify({"message":"added to the queue"}),201

@addchats_bp.route('/addchatsgs')
def addchatgs():
    #form=QualityForm()
    keys = os.environ["SHEET_SERVICE_ACCOUNT"]
    creds_dict = json.loads(keys)
    sa = gspread.service_account_from_dict(creds_dict)
    #sa= gspread.service_account(keys)
    sh= sa.open("Quality Auditing Queue")
    wks=sh.worksheet("Queue")
    queue= wks.get_all_records()
    for dict in queue:
        new_dict = Auditing(cx_agent=dict['cx_agent'] ,supervisor=dict["supervisor"],convo_link=dict['convo_link'],date_of_conversation=dict['date_of_conversation'],quality_agent=dict['quality_agent'],label=dict['label'],assigned_group=dict['assigned_group'])
        db.session.add(new_dict)
        db.session.commit()
        flash('Chats Added successfully using google sheets')
    return redirect(url_for('addchats.add_chats'))

@addchats_bp.route('/chatdelete/<int:id>')
@login_required
def chatdelete(id):
    chats_to_delete=Auditing.query.get_or_404(id)
    form=QualityForm()
    cx_agent=None
    supervisor=None
    convo_link=None
    date_of_conversation=None
    our_chats= Auditing.query.order_by(Auditing.id)
    try:

        db.session.delete(chats_to_delete)
        db.session.commit()
        
        our_chats= Auditing.query.order_by(Auditing.id)
        return render_template("auditing.html",form=form,cx_agent=cx_agent,supervisor=supervisor,convo_link=convo_link,date_of_conversation=date_of_conversation,ourchats=our_chats)
    except:
        return render_template("auditing.html",form=form,cx_agent=cx_agent,supervisor=supervisor,convo_link=convo_link,date_of_conversation=date_of_conversation,ourchats=our_chats)
    
@addchats_bp.route('/deleteall')
@login_required
def deleteall():
    for class_instance in Auditing.query.all():
        deletell=class_instance
        db.session.delete(deletell)
        db.session.commit()
    return redirect(url_for('addchats.add_chats'))