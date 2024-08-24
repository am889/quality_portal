from flask import Blueprint,send_file
from app.database.models import *
from app.forms.form import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pandas as pd
import io
from datetime import datetime, time, timedelta


cx_dashboardbp= Blueprint('cx_dashboardbp',__name__)

@cx_dashboardbp.route('/cxdashboard',methods= ['GET','POST'])
def cx_dashboard():
    form = FilterForm()
    if form.validate_on_submit():
        
        start_date = form.start_date.data
        end_date = form.end_date.data
        print(start_date)
        return redirect(f'/cxdashboard/{start_date}/{end_date}')
    today_date = datetime.now().date()
    start_time = time(0, 0)  # 12 am
    end_time = time(23, 59, 59)  # 11:59:59 pm

    # Convert today_date to a datetime object
    today_datetime = datetime.combine(today_date, time())

    # Format the datetime as a string before filtering
    formatted_start_time = (today_datetime + timedelta(hours=start_time.hour, minutes=start_time.minute)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    formatted_end_time = (today_datetime + timedelta(hours=end_time.hour, minutes=end_time.minute)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # Get the distinct quality agents for today
    distinct_quality_agents = Audited.query.with_entities(Audited.cx_agent).filter(
        Audited.date == today_date,
        Audited.time_stamp.between(formatted_start_time, formatted_end_time)
    ).distinct()

    
    # Create a list of dictionaries to store the count for each user
    user_counts = []
    for agent in distinct_quality_agents:
        user_count = Audited.query.filter(
            Audited.cx_agent == agent[0],
            Audited.date == today_date,
            Audited.time_stamp.between(formatted_start_time, formatted_end_time)
            ).count()

        # Store the count in the list as a dictionary with the quality agent and count
        user_counts.append({'cx_agent': agent[0], 'count': user_count})
    chart=pd.DataFrame.from_dict(user_counts)
    print(chart)
    chart=pd.DataFrame.from_dict(user_counts)
    print(chart)
    img = io.BytesIO()
    plt.figure(figsize=(10, 15))
    if not user_counts:
        user_counts = [{'cx_agent': 'No Data', 'count': 0}]
    else:
        plt.bar(chart['cx_agent'], chart['count'])
    plt.xlabel('cx_agent')
    plt.ylabel('Count')
    plt.title('Counts of Quality Agents')
    plt.tight_layout()
    plt.savefig(img, format='png')
    return render_template("cx_dashboard.html",user_counts=user_counts,form=form,chart_url=url_for('cx_dashboardbp.cx_chart', start_date=today_date, end_date=today_date))  


@cx_dashboardbp.route('/cxdashboard/<start_date>/<end_date>',methods=['GET','POST'])
def dashboardfilter(start_date,end_date):
    form = FilterForm()
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        print(start_date)
        return redirect(f'/cxdashboard/{start_date}/{end_date}')
    

    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')

    # Get start and end times
    start_time = time(0, 0)  # 12 am
    end_time = time(23, 59, 59)  # 11:59:59 pm

    # Format the datetime as a string before filtering
    formatted_start_time = (start_datetime + timedelta(hours=start_time.hour, minutes=start_time.minute)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    formatted_end_time = (end_datetime + timedelta(hours=end_time.hour, minutes=end_time.minute)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # Get the distinct quality agents for the specified date range
    distinct_quality_agents = Audited.query.with_entities(Audited.cx_agent).filter(
        Audited.date.between(start_date, end_date),
        Audited.time_stamp.between(formatted_start_time, formatted_end_time)
    ).distinct()

    # Create a list of dictionaries to store the count for each user
    user_counts = []
    for agent in distinct_quality_agents:
        user_count = Audited.query.filter(
            Audited.cx_agent == agent[0],
            Audited.date.between(start_date, end_date),
            Audited.time_stamp.between(formatted_start_time, formatted_end_time)
        ).count()

        # Store the count in the list as a dictionary with the quality agent and count
        user_counts.append({'cx_agent': agent[0], 'count': user_count})
    chart=pd.DataFrame.from_dict(user_counts)
    print(chart)
    img = io.BytesIO()
    plt.figure(figsize=(5, 6))
    if  not user_counts:
        user_counts = [{'cx_agent': 'No chats', 'count': 0}]

    else:
        plt.bar(chart['cx_agent'], chart['count'])

    plt.xlabel('Quality Agent')
    plt.ylabel('Count')
    plt.title('Counts of Quality Agents')
    plt.tight_layout()
    plt.savefig(img, format='png')
    

        
    return render_template("Dashboard.html", user_counts=user_counts, form=form,chart_url=url_for('cx_dashboardbp.cx_chart', start_date=start_date, end_date=end_date))

@cx_dashboardbp.route('/cx_chart.png')
def cx_chart():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
    
    start_time = time(0, 0)  # 12 am
    end_time = time(23, 59, 59)  # 11:59:59 pm

    formatted_start_time = (start_datetime + timedelta(hours=start_time.hour, minutes=start_time.minute)).strftime("%Y-%m-%d %H:%M:%S")
    formatted_end_time = (end_datetime + timedelta(hours=end_time.hour, minutes=end_time.minute)).strftime("%Y-%m-%d %H:%M:%S")

    distinct_quality_agents = Audited.query.with_entities(Audited.cx_agent).filter(
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
        user_counts.append({'cx_agent': agent[0], 'count': user_count})

    chart = pd.DataFrame.from_dict(user_counts)
    if not user_counts:
        user_counts = [{'cx_agent': 'No Data', 'count': 0}]
    

    img = io.BytesIO()
    fig, ax = plt.subplots(figsize=(5, 6))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    ax.bar(chart['cx_agent'], chart['count'],color='yellow')

    ax.set_xlabel('Quality Agent',color='white')
    ax.set_ylabel('Count',color='white')
    ax.set_title('Audited Chats',color='white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white') 
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)

    return send_file(img, mimetype='image/png')
