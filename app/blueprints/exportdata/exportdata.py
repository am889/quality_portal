from flask import Flask,render_template, url_for,redirect,flash,request, jsonify, send_from_directory,Blueprint,Response
from app.forms.form import *
from app.database.models import *


exportdata_bp = Blueprint('exportdata',__name__)


@exportdata_bp.route('/export_data',methods=['GET', 'POST'])
@login_required
def import_data():
    if current_user.role=="Admin":

        form = FilterForm()
        if form.validate_on_submit():
            start_date = form.start_date.data
            end_date = form.end_date.data

            users = Audited.query.filter(Audited.date.between(start_date, end_date))

            csv_data = 'id,cx_agent,supervisor,convo_link,quality_agent,label,assigned_group,assigned_date,date_of_conversation,time_stamp,Identification_of_contact,Identification_of_contact_comment,Information_Accuracy,Information_Accuracy_comment,Proactively_providing_solution,Proactively_providing_solution_comment,Setting_correct_Follow_up,Setting_correct_Follow_up_comment,Contact_reason,Contact_reason_comment,Documented_notes_information,Documented_notes_information_comment,Ticket_escalation,Ticket_escalation_comment,Adherence_to_procedures,Adherence_to_procedures_comment,Opening_Closing,Opening_Closing_comment,Format_Writing_Professionalism,Format_Writing_Professionalism_comment,Apologizing_Empathy,Apologizing_Empathy_comment,Active_Acknowledgment,Active_Acknowledgment_comment,Conversation_Control,Conversation_Control_comment,Confidentiality,Confidentiality_comment,observation_recommendation\n'

            csv_data += '\n'.join([
                ','.join([
                    str(user.id),
                    user.cx_agent.replace(",", "-"),
                    user.supervisor.replace(",", "-"),
                    user.convo_link,
                    user.quality_agent.replace(",", "-"),
                    user.label.replace(",", "-"),
                    user.assigned_group.replace(",", "-"),
                    str(user.assigned_date),
                    str(user.date_of_conversation),
                    str(user.time_stamp),
                    user.Identification_of_contact.replace(",", "-"),
                    user.Identification_of_contact_comment.replace(",", "-"),
                    user.Information_Accuracy.replace(",", "-"),
                    user.Information_Accuracy_comment.replace(",", "-"),
                    user.Proactively_providing_solution.replace(",", "-"),
                    user.Proactively_providing_solution_comment.replace(",", "-"),
                    user.Setting_correct_Follow_up.replace(",", "-"),
                    user.Setting_correct_Follow_up_comment.replace(",", "-"),
                    user.Contact_reason.replace(",", "-"),
                    user.Contact_reason_comment.replace(",", "-"),
                    user.Documented_notes_information.replace(",", "-"),
                    user.Documented_notes_information_comment.replace(",", "-"),
                    user.Ticket_escalation.replace(",", "-"),
                    user.Ticket_escalation_comment.replace(",", "-"),
                    user.Adherence_to_procedures.replace(",", "-"),
                    user.Adherence_to_procedures_comment.replace(",", "-"),
                    user.Opening_Closing.replace(",", "-"),
                    user.Opening_Closing_comment.replace(",", "-"),
                    user.Format_Writing_Professionalism.replace(",", "-"),
                    user.Format_Writing_Professionalism_comment.replace(",", "-"),
                    user.Apologizing_Empathy.replace(",", "-"),
                    user.Apologizing_Empathy_comment.replace(",", "-"),
                    user.Active_Acknowledgment.replace(",", "-"),
                    user.Active_Acknowledgment_comment.replace(",", "-"),
                    user.Conversation_Control.replace(",", "-"),
                    user.Conversation_Control_comment.replace(",", "-"),
                    user.Confidentiality.replace(",", "-"),
                    user.Confidentiality_comment.replace(",", "-"),
                    '"' + user.observation_recommendation.replace("\n", " ").replace(",", "-") + '"' if user.observation_recommendation else ''
                ]) 
                for user in users]
            )
            
            response = Response(csv_data, mimetype='text/csv')
            response.headers['Content-Disposition'] = f'attachment; filename=Audited_Chats_from_{start_date}_to_{end_date}.csv'
            return response

    else:
        return redirect(url_for('admin.adminaccess'))

    return render_template('exportdata.html',form=form)
