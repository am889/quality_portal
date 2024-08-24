from flask import render_template, Blueprint

notfound_bp = Blueprint('notfound',__name__)
#error handler
@notfound_bp.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404