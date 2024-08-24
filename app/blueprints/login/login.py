from flask import Blueprint
from flask_login import UserMixin, login_user,LoginManager,login_required,logout_user,current_user
from app.database.models import *
from flask_jwt import jwt_required
from app.forms.form import LoginForm
login_bp = Blueprint('login',__name__)

login_manager= LoginManager()
login_manager.login_view = 'login.login'





# #Add Chats Form
# def get_default():
#     datetime.datetime.utcnow().timestamp()

#login route public
@login_bp.route('/login/', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user= Users.query.filter_by(email=form.email.data).first()
        if user:
            if form.password.data== user.password:
                login_user(user)
                flash("Login Successfully!")
                
                return redirect(url_for('home.Home'))
            else:
                flash("Wrong Password, Try Again!")
    
    email= ''
    password ='' 
    email= form.email.data
    form.email.data=''
    password= form.password.data
    form.password.data=''
    flash('You are logged in')
    return render_template("Login.HTML",form=form,email= email,password=password)




#create Logout
@login_bp.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for('login.login'))