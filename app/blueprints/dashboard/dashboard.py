from flask import Blueprint,render_template,make_response, send_file
from app.database.models import *
from app.forms.form import *
import csv
from datetime import datetime, time, timedelta
import pandas as pd
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pandas as pd
import io
from queue_handling.classes import Dashboard


dashboard_bp = Blueprint('dashboard',__name__)

@dashboard_bp.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    
    form = FilterForm()
    dashboard=Dashboard(
        start_date=datetime.now().date(),
        end_date=datetime.now().date(),
        auditeddb=Audited,
        form=form)
    dashboard.user_counts.clear()
    if form.validate_on_submit():
        
        start_date = form.start_date.data
        end_date = form.end_date.data
        print(start_date)
        return redirect(f'/dashboard/{start_date}/{end_date}')
    dashboard.default_dashboard()
    if dashboard.user_counts:
        chart = pd.DataFrame.from_dict(dashboard.user_counts)
        print(chart)
        img = io.BytesIO()
        plt.figure(figsize=(5, 6))
        plt.bar(chart['quality_agent'], chart['count'])
        plt.xlabel('Quality Agent')
        plt.ylabel('Count')
        plt.title('Counts of Quality Agents')
        plt.tight_layout()
        plt.savefig(img, format='png')
        img.seek(0)
    else:
        img = None
        dashboard.user_counts = [{'quality_agent': 'No Data', 'count': 0}]
    
    return render_template(
        'dashboard.html',
        user_counts=dashboard.user_counts,
        form=form,
        chart_url=url_for('dashboard.chart_image', start_date=dashboard.start_date, end_date=dashboard.end_date)
    )

@dashboard_bp.route('/dashboard/<start_date>/<end_date>',methods=['GET','POST'])
def dashboardfilter(start_date,end_date):
    form = FilterForm()
    dashboard=Dashboard(
        start_date=start_date,
        end_date=end_date,
        auditeddb=Audited,
        form=form)
    dashboard.user_counts.clear()
    dashboard.filtered_dashboard()

    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        print(start_date)
        return redirect(f'/dashboard/{start_date}/{end_date}')
    
    if dashboard.user_counts:
        chart = pd.DataFrame.from_dict(dashboard.user_counts)
        print(chart)
        img = io.BytesIO()
        plt.figure(figsize=(5, 6))
        plt.bar(chart['quality_agent'], chart['count'])
        plt.xlabel('Quality Agent')
        plt.ylabel('Count')
        plt.title('Counts of Quality Agents')
        plt.tight_layout()
        plt.savefig(img, format='png')
        img.seek(0)
    else:
        img = None
        # dashboard.user_counts = [{'quality_agent': 'No Data', 'count': 0}]
    

        
    return render_template("Dashboard.html", user_counts=dashboard.user_counts, form=form,chart_url=url_for('dashboard.chart_image', start_date=dashboard.start_date, end_date=dashboard.end_date))

@dashboard_bp.route('/chart.png')
def chart_image():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
    
    start_time = time(0, 0)  # 12 am
    end_time = time(23, 59, 59)  # 11:59:59 pm

    formatted_start_time = (start_datetime + timedelta(hours=start_time.hour, minutes=start_time.minute)).strftime("%Y-%m-%d %H:%M:%S")
    formatted_end_time = (end_datetime + timedelta(hours=end_time.hour, minutes=end_time.minute)).strftime("%Y-%m-%d %H:%M:%S")

    distinct_quality_agents = Audited.query.with_entities(Audited.quality_agent).filter(
        Audited.date.between(start_date, end_date),
        Audited.time_stamp.between(formatted_start_time, formatted_end_time)
    ).distinct()

    user_counts = []
    for agent in distinct_quality_agents:
        user_count = Audited.query.filter(
            Audited.quality_agent == agent[0],
            Audited.date.between(start_date, end_date),
            Audited.time_stamp.between(formatted_start_time, formatted_end_time)
        ).count()
        user_counts.append({'quality_agent': agent[0], 'count': user_count})

    chart = pd.DataFrame.from_dict(user_counts)
    if not user_counts:
        user_counts = [{'quality_agent': 'No Data', 'count': 0}]
    

    img = io.BytesIO()
    fig, ax = plt.subplots(figsize=(5, 6))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    ax.bar(chart['quality_agent'], chart['count'],color='yellow')

    ax.set_xlabel('Quality Agent',color='white')
    ax.set_ylabel('Count',color='white')
    ax.set_title('Audited Chats',color='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white') 
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)

    return send_file(img, mimetype='image/png')