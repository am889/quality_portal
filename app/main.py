
from flask import Flask,render_template
from flask_migrate import Migrate
from app import create_app

# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI']= dbconnection

# #Secret key
# app.config['SECRET_KEY']= secret_code
# #create a model

# db.init_app(app)
# migrate = Migrate(app, db)
# login_manager.init_app(app)
# @login_manager.user_loader
# def load_user(user_id):
#     return Users.query.get(int(user_id))

app =create_app()
# app.register_blueprint(models_bp)

# run the app

