from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.database.db_connection import dbconnection
from .database.models import *
from .database.db_connection import dbconnection,jwt
from .secretcode import secret_code
from .forms.form import *
from .database.models import db,Users
from .blueprints.addchats.addchats import addchats_bp
from .blueprints.exportdata.exportdata import exportdata_bp
from .blueprints.dashboard.dashboard import dashboard_bp
from .blueprints.login.login  import login_bp,login_manager
from .blueprints.register.register import register_bp
from .blueprints.audit.audit import audit_bp
from .blueprints.admin.admin import admin_bp
from .blueprints.notfound.notfound import notfound_bp
from .blueprints.home.home import home_bp
from .blueprints.auth.auth import auth_bp
from .blueprints.cx_dashboard.cx_dashboard import cx_dashboardbp

def create_app(dbconnection=dbconnection):
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI']= dbconnection

    #Secret key
    app.config['SECRET_KEY']= secret_code
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['JWT_SECRET_KEY']="4f0b8c0d98f33ce62a5eb13dd90000780fd3ca0ba2094524d09fc28d62657f5e"
    app.config['JWT_ACCESS_TOKEN_EXPIRES']=timedelta(minutes=30)
    
    #create a model
#     Base = declarative_base()

# #Initialize Database
#     db=SQLAlchemy(model_class=Base)

    db.init_app(app)
    jwt.init_app(app)
    @jwt.additional_claims_loader
    def make_additiona_calims(identity):
        if identity=="ali.mohamed@thndr.app":
            return{"is_admin":True}
        return{"is_admin":False}


    migrate = Migrate(app, db)
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))
    app.register_blueprint(auth_bp)
    app.register_blueprint(addchats_bp)
    app.register_blueprint(cx_dashboardbp)
    app.register_blueprint(exportdata_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(audit_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(notfound_bp)
    app.register_blueprint(home_bp)
    return app