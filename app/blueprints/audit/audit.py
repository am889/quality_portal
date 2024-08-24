from flask import Blueprint
from sqlalchemy import update
from app.database.models import *
from app.blueprints.login.login import *
from app.forms.form import *
from queue_handling.classes import Start_audit, Update_db_int
audit_bp = Blueprint('audit',__name__)



@audit_bp.route('/audit',methods=['GET','POST'])
@login_required 
def audit():
    Session = sessionmaker(bind=engine)
    session = Session()
    return Start_audit.assign_chats(current_quality_agent=current_user.email,chatsdb=Auditing,session=session,db=db)


@audit_bp.route('/audit/<int:id>',methods=['GET','POST'])
@login_required
def audits(id):
    form= AuditForm() 
    Session = sessionmaker(bind=engine)
    session = Session()
    return  Start_audit.audit(current_quality_agent=current_user.email,id=id,form=form,session=session,db=db,chatsdb=Audited,auditingdb=Auditing)


# @audit_bp.route('/update_db')
# def update_db():
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     for audits in session.query(Audited).all():
#         chat=Update_db_int(Active_Listining=audits.Active_Listining,Identification_of_contact=audits.Identification_of_contact,Information_Accuracy=audits.Information_Accuracy,Proactively_providing_solution=audits.Proactively_providing_solution)
#         return chat.update_db()
# @app.route('/deleteaudited')
# @login_required
# def deleteaudited():
#     for class_instance in Audited.query.all():
#         deletell=class_instance
#         db.session.delete(deletell)
#         db.session.commit()
#     return redirect(url_for('add_chats'))
