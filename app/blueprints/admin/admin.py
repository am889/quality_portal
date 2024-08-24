from flask import Blueprint,render_template
from app.blueprints.login.login import *
from app.database.models import *

admin_bp = Blueprint('admin',__name__)

@admin_bp.route('/adminaccess')
@login_required
def adminaccess():
    return render_template('test.html')