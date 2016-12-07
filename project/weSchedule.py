#!/usr/local/bin/python2.7
'''Kelly Kung and Jason Lan'''
'''CS 304'''
'''WeSchedule'''
#This is the file that links the html form to the data
import os, sys, datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
import weSchedule_data
from datetime import datetime, timedelta

app = Flask(__name__)
'''need secret key for flash message'''
app.secret_key = 'rosebud'


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        res = weSchedule_data.login(request.form['user-name'],request.form['user-password'])
        if res == -1:
            return render_template('login.html', msg = 'Username not found in database')
        elif res == -2:
            return render_template('login.html', msg = 'Wrong password')
        else:
            session['username'] = res['username']
            session['UID'] = res["UID"]
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout/')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   session.pop('UID', None)
   return redirect(url_for('index'))

@app.route('/register/', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        res = weSchedule_data.register(request.form['user-name'],request.form['user-password'])
        if res == -1:
            return render_template('register.html', msg = 'The username is taken. Please choose a different one.')
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/dashboard/', methods = ['GET', 'POST'])
def dashboard():
    if 'username' in session:
        username = session['username']
        return render_template('account.html', UserName = username)
    else:
        return redirect(url_for('index'))

@app.route('/createEvent/', methods = ['GET', 'POST'])
def createEvent():
    meth = request.method
    conn = weSchedule_data.getConn()
    
    if meth == 'POST':
        if 'start-date' in request.form and 'end-date' in request.form:
            start_date = weSchedule_data.convertDate(request.form['start-date'], "%m/%d/%Y")
            end_date = weSchedule_data.convertDate(request.form['end-date'], "%m/%d/%Y");
            
            organizer_name = (request.form['Organizer Name'])
            event_name = (request.form['Event Name'])
        
            if weSchedule_data.getUserData(organizer_name.lower()) == None:
                weSchedule_data.insertUser(organizer_name, "yes")

            weSchedule_data.insertEvent(event_name, start_date, end_date, organizer_name)
            event = weSchedule_data.getEvent(event_name, organizer_name)
            
            #now we insert each time using a for loop
            date = datetime.strptime(str(start_date), '%Y-%m-%d')
            print "start date is " + str(start_date)
            print "concat " +str(date)
            
            while date != datetime.strptime(str(end_date), '%Y-%m-%d'):
                weSchedule_data.insertAvailability(event_name, organizer_name, weSchedule_data.convertDate(date.strftime('%Y-%m-%d'), '%Y-%m-%d'))
                date = date + timedelta(days = 1)
            return redirect(url_for('confirmation', event_ID = event['eventID'], UID = event['UID']))
            
        else: 
            flash ('Please fill out all the fields')
            return render_template('index.html')
            

    return render_template('index.html')
        
    
@app.route('/confirmation/eventID<int:event_ID>/UID<int:UID>')
def confirmation(event_ID, UID):
    url = "cs.wellesley.edu:" + str(os.getuid()) + "/confirmation/eventID" + str(event_ID) + "/UID" + str(UID)
    event_name = weSchedule_data.getEventName(event_ID)['event_name']
    creator_name = weSchedule_data.getUserName(UID)['user_name']
    dates = weSchedule_data.getDates(event_ID, UID)
    final_dates = []
    for date in dates:
        final_dates.append(date['availability'].strftime('%Y-%m-%d'))
    return render_template('eventConfirmation.html', url = url, event_name = event_name, creator_name = creator_name, dates = final_dates)
    

if __name__ == '__main__':
    app.debug = True
    port = os.getuid()
    print('Running on port ' + str(port))
    app.run('0.0.0.0', port)

    