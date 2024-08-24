from flask import Blueprint
from app.database.models import *
from app.forms.form import *

register_bp = Blueprint('register',__name__)


#register
@register_bp.route('/register',methods=['GET','POST'])
@login_required
def add_user():
    if current_user.role=="Admin":
        form=UserForm()
        first_name=None
        second_name=None
        password=None
        email=None
        role=None
        our_users= Users.query.order_by(Users.id)

        if form.validate_on_submit():
            user=Users.query.filter_by(email=form.email.data).first()

            if user is None:
                user=Users(first_name=form.first_name.data,second_name=form.second_name.data,email=form.email.data,password=form.password.data,role=form.role.data)
                db.session.add(user)
                db.session.commit()

            first_name=form.first_name.data
            second_name=form.second_name.data
            email=form.email.data
            password=form.password.data
            role=form.role.data
            form.password.data=''
            form.second_name.data=''
            form.first_name.data=''
            form.email.data=''
            form.role.data=''
            flash('User Added successfully!')

            our_users= Users.query.order_by(Users.id)
    elif current_user.role=="User":
        return redirect(url_for('admin.adminaccess'))
 
    return render_template("register.html",form=form,first_name=first_name,second_name=second_name,password=password,email=email,ourusers=our_users,role=role)

#delete users
@register_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    user_to_delete=Users.query.get_or_404(id)
    form=UserForm()
    first_name=None
    second_name=None
    password=None
    email=None
    our_users= Users.query.order_by(Users.id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        
        our_users= Users.query.order_by(Users.id)
        return render_template("register.html",form=form,first_name=first_name,second_name=second_name,password=password,email=email,ourusers=our_users)
#login route public
    except:
        return render_template("register.html",form=form,first_name=first_name,second_name=second_name,password=password,email=email,ourusers=our_users)
    

#update users route  
@register_bp.route('/update/<int:id>',methods=['GET','POST'])
@login_required
def update(id):
    form=UserForm()
    name_to_update=Users.query.get_or_404(id)
    if request.method=="POST":
        name_to_update.first_name=request.form['first_name']
        name_to_update.second_name=request.form['second_name']
        name_to_update.email=request.form['email']
        name_to_update.password=request.form['password']
        try:
            db.session.commit()
            return render_template('update.html',name_to_update=name_to_update,form=form)
        except:
            flash('cannot update')
    else:
         return render_template('update.html',name_to_update=name_to_update,form=form)