from app.database.models import *
from abc import ABC,abstractmethod
from flask import Flask,request,jsonify,redirect


class Add_chats:
    all_chats = []

    def __init__(self, chat_id, cx_agent,quality_agent,supervisor,label,assigned_group,convo_link,date_of_conversation):
        self.chat_id = chat_id
        self.quality_agent= quality_agent
        self.supervisor = supervisor
        self.label =label
        self.assigned_group =assigned_group
        self.cx_agent =cx_agent
        self.convo_link=convo_link
        self.date_of_conversation=date_of_conversation
        Add_chats.all_chats.append(self)

    @classmethod
    def read_api(cls, chats):
        for chat in chats:
            chat_id = chat["chat_id"]
            cx_agent = chat["cx_agent"]
            quality_agent = chat["quality_agent"]
            supervisor = chat["supervisor"]
            label = chat["label"]
            assigned_group = chat["assigned_group"]
            convo_link = chat["convo_link"]
            date_of_conversation = chat["date_of_conversation"]
            cls(chat_id, cx_agent, quality_agent, supervisor, label, assigned_group,convo_link,date_of_conversation)

    @classmethod
    def get_chat_by_id(cls, chat_id):
        for chat in cls.all_chats:
            if chat.chat_id == chat_id:
                chat1=chat
                return chat1
        return None
    @classmethod
    def start_auditing(cls,quality_agent):
        for chat in cls.all_chats:
            if chat.quality_agent ==quality_agent:
                return chat
    
    @classmethod
    def move_chats_to_db(cls,table,db):
        for chat in cls.all_chats:
            chats=table(cx_agent=chat.cx_agent,supervisor=chat.supervisor,convo_link=chat.convo_link,date_of_conversation=chat.date_of_conversation,quality_agent=chat.quality_agent,label=chat.label,assigned_group=chat.assigned_group)
            db.session.add(chats)
            db.session.commit()
    def __str__(self):
        return f"Chat ID: {self.chat_id}, User ID: {self.user_id}"

    def __repr__(self):
        return f"Chat ID: {self.chat_id}, User ID: {self.user_id}, Message: {self.message}"


class Move_chats_to_db(Add_chats):
    def __init__(self, chat_id, user_id, message, autofail, recommendation):
        super().__init__(chat_id, user_id, message)
        self.autofail = autofail
        self.recommendation = recommendation

    def save_to_db(self, chat_id):
        chat = Add_chats.get_chat_by_id(chat_id)
        if chat:
            print(f"Saving chat {chat.chat_id} to database")
        else:
            print("No Chat Check the ID")


class Start_audit:
    
    selected_chat=[]
    @staticmethod
    def assign_chats(current_quality_agent,chatsdb,session,db):
        audit_assigned_chat = session.query(chatsdb).filter_by(quality_agent=current_quality_agent).first()
        audit_unassigned_chat = session.query(chatsdb).filter_by(quality_agent='').first()
        Start_audit.selected_chat.append(audit_assigned_chat)
        if audit_assigned_chat:
            audit_assigned_chat.assigned_date = datetime.now()
            chat_id =audit_assigned_chat.id
            return redirect(f'audit/{chat_id}')
        elif audit_unassigned_chat:
            audit_unassigned_chat.email = current_quality_agent
            audit_unassigned_chat.assigned_date = datetime.now()
            session.commit()
            return redirect(f'audit/{audit_unassigned_chat.id}')
        else:
            flash("Good job There's no chats right now")
            return render_template('nochats.html')

    
    

    @staticmethod
    def audit(current_quality_agent,chatsdb,session,db,id,form,auditingdb):
        audit_assigned_chat = session.query(auditingdb).filter_by(id=id).first()
        print(audit_assigned_chat.id)
        # if audit_assigned_chat.skip==False:
        #         audit_assigned_chat.assigned_date=datetime.now()
        #         session.commit()
        #         audits=Auditing.query.filter_by(id=id).first()
        #         print('first step')
        #         return render_template('audit.html',form=form,chat_to_update=audit_assigned_chat)
        #     # elif audited:
        #     #     return render_template('audit.html',form=form,chat_to_update=audited)
        # elif audit_assigned_chat.skip ==True:
        #         audit_assigned_chat.assigned_date=datetime.now()
        #         session.commit()
        #         audits=Auditing.query.filter_by(id=id).first()
        #         print('first step')
        # else:
        #         flash("Good job There's no chats right now")
        #         return render_template('nochats.html')
        if request.method=='GET':
            return render_template('audit.html',form=form,chat_to_update=audit_assigned_chat)

        if request.method=='POST':
            print('POSTED')
            audited_chat = chatsdb(
            cx_agent=form.cx_agent.data,
            supervisor=form.supervisor.data,
            convo_link=form.convo_link.data,
            date_of_conversation=form.date_of_conversation.data,
            quality_agent=form.quality_agent.data,
            label=form.label.data,
            assigned_group=form.assigned_group.data,
            Active_Listining=form.Active_Listining.data,
            Active_Listining_comment=form.Active_Listining_comment.data,
            Identification_of_contact=form.Identification_of_contact.data,
            Identification_of_contact_comment=form.Identification_of_contact_comment.data,
            Information_Accuracy=form.Information_Accuracy.data,
            Information_Accuracy_comment=form.Information_Accuracy_comment.data,
            Proactively_providing_solution=form.Proactively_providing_solution.data,
            Proactively_providing_solution_comment=form.Proactively_providing_solution_comment.data,
            Format_Writing_Professionalism=form.Format_Writing_Professionalism.data,
            Format_Writing_Professionalism_comment=form.Format_Writing_Professionalism_comment.data,
            Documented_notes_information=form.Documented_notes_information.data,
            Documented_notes_information_comment=form.Documented_notes_information_comment.data,
            Ticket_escalation=form.Ticket_escalation.data,
            Ticket_escalation_comment=form.Ticket_escalation_comment.data,
            Adherence_to_procedures=form.Adherence_to_procedures.data,
            Adherence_to_procedures_comment=form.Adherence_to_procedures_comment.data,
            Opening_Closing=form.Opening_Closing.data,
            Opening_Closing_comment=form.Opening_Closing_comment.data,
            Apologizing_Empathy=form.Apologizing_Empathy.data,
            Apologizing_Empathy_comment=form.Apologizing_Empathy_comment.data,
            Active_Acknowledgment=form.Active_Acknowledgment.data,
            Active_Acknowledgment_comment=form.Active_Acknowledgment_comment.data,
            Conversation_Control=form.Conversation_Control.data,
            Conversation_Control_comment=form.Conversation_Control_comment.data,
            Confidentiality=form.Confidentiality.data,
            Confidentiality_comment=form.Confidentiality_comment.data,
            auto_fail=form.auto_fail.data,
            observation_recommendation=form.observation_recommendation.data,
            assigned_date=form.assigned_date.data,
            Setting_correct_Follow_up=form.Setting_correct_Follow_up.data,
            Setting_correct_Follow_up_comment=form.Setting_correct_Follow_up_comment.data,
            Contact_reason=form.Contact_reason.data,
            Contact_reason_comment=form.Contact_reason_comment.data,
            auditing_id=form.auditing_id.data,
            time_stamp=datetime.now(),
            date=datetime.today()
        )

            if form.submit_button_1.data:

                try:
                    # Add the new audit entry
                    session.add(audited_chat)
                    print('step3')
                    session.delete(audit_assigned_chat)
                    print('step 4')
                    session.commit()
                    # db.session.add(audited_chat)
                    # db.session.commit()

                    # # Remove the assigned chat after adding the new audit entry
                    # db.session.delete(audit_assigned_chat)
                    # db.session.commit()

                    return redirect(url_for('audit.audit'))
    
                except:
                    return "Error While submiting button 1"
            elif form.submit_button_2.data:
                try:
                    session.add(audited_chat)
                    session.delete(audit_assigned_chat)
                    session.commit()
                    return redirect(url_for('home.Home'))
                except:
                    return "Error While redirect to next page"
            elif form.submit_button_3.data:
                try:
                    # audits=Auditing.query.filter_by(id=id).first()
                    audit_assigned_chat.skip = True
                    session.commit()
                    return redirect(url_for('audit.audit'))
            
                except:
                    return "Can't Skip this Chat" 
  
        # return render_template('audit.html', form=form, chat_to_update=audit_assigned_chat)
          
class Dashboard:

    def __init__(self,start_date,end_date,auditeddb,form,today_date=datetime.now().date(),start_time=time(0,0),end_time=time(23,59,59)):
        self.start_date=start_date
        self.end_date=end_date
        self.today_date=today_date
        self.start_time=start_time
        self.end_time=end_time
        self.auditeddb=auditeddb
        self.form=form
        self.user_counts = []


    def filtered_dashboard(self):
        start_datetime = datetime.strptime(self.start_date, '%Y-%m-%d')

        end_datetime = datetime.strptime(self.end_date, '%Y-%m-%d')
        formatted_start_time =(start_datetime+timedelta(hours=self.start_time.hour,minutes=self.start_time.minute)).strftime(
            '%Y-%m-%d %H:%M:%S')
        formatted_end_time =(end_datetime+timedelta(hours=self.end_time.hour,minutes=self.end_time.minute)).strftime(
            '%Y-%m-%d %H:%M:%S')
        self.filterdb2(formatted_start_time=formatted_start_time,formatted_end_time=formatted_end_time)


    def default_dashboard(self):
        today_datetime= datetime.combine(self.today_date,time())
        formatted_start_time =(today_datetime+timedelta(hours=self.start_time.hour,minutes=self.start_time.minute)).strftime(
            '%Y-%m-%d %H:%M:%S')
        formatted_end_time =(today_datetime+timedelta(hours=self.end_time.hour,minutes=self.end_time.minute)).strftime(
            '%Y-%m-%d %H:%M:%S')
        self.filterdb(formatted_start_time=formatted_start_time,formatted_end_time=formatted_end_time)


    def filterdb(self,formatted_start_time,formatted_end_time):
        distinct_quality_agents=self.auditeddb.query.with_entities(self.auditeddb.quality_agent).filter(
            self.auditeddb.date ==self.today_date,
            self.auditeddb.time_stamp.between(formatted_start_time,formatted_end_time)
        ).distinct()
        self.countchats(distinct_quality_agents=distinct_quality_agents,formatted_start_time=formatted_start_time,formatted_end_time=formatted_end_time)


    def filterdb2(self,formatted_start_time,formatted_end_time):
        distinct_quality_agents=self.auditeddb.query.with_entities(self.auditeddb.quality_agent).filter(
            self.auditeddb.date.between(self.start_date,self.end_date),
            self.auditeddb.time_stamp.between(formatted_start_time,formatted_end_time)
        ).distinct()
        self.countchats2(distinct_quality_agents=distinct_quality_agents,formatted_start_time=formatted_start_time,formatted_end_time=formatted_end_time)


    def countchats(self,distinct_quality_agents,formatted_start_time,formatted_end_time):
        for agent in distinct_quality_agents:
            user_count = self.auditeddb.query.filter(
                self.auditeddb.quality_agent == agent[0],
                self.auditeddb.date == self.today_date,
                self.auditeddb.time_stamp.between(formatted_start_time,formatted_end_time)
            ).count()
            self.user_counts.append({'quality_agent':agent[0],'count':user_count})


    def countchats2(self,distinct_quality_agents,formatted_start_time,formatted_end_time):
        for agent in distinct_quality_agents:
            user_count = self.auditeddb.query.filter(
                self.auditeddb.quality_agent == agent[0],
                self.auditeddb.date.between(self.start_date,self.end_date),
                self.auditeddb.time_stamp.between(formatted_start_time,formatted_end_time)
            ).count()
            self.user_counts.append({'quality_agent':agent[0],'count':user_count})



# class Update_db_int:
#     def __init__(self, **kwargs):
#         variables = [
#              'Active_Listining', 
#             'Identification_of_contact', 'Information_Accuracy', 
#             'Proactively_providing_solution'
#         ]
        
#         for var in variables:
#             setattr(self, var, kwargs.get(var))

#     @classmethod
#     def update_db(cls):
#         for i in cls.variables:
#             if i == 'Zero Pinted':
#                 pass
#         # for i in cls:
#         #     print (i)
#             # if i =="Zero Pointed":
#             #     i = 0
#             # elif i =="Full Pointed":
#             #     i = 1




