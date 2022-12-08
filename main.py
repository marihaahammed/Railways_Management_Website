from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from ast import literal_eval
import MySQLdb.cursors
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'yshaikh'
app.config['MYSQL_PASSWORD'] = 'dJTy7cg2'
app.config['MYSQL_DB'] = 'yshaikh'

# Intialize MySQL
mysql = MySQL(app)

@app.route('/home', methods=['GET', 'POST'])
def home():
     msg = ''
     return render_template('railways.html', msg = msg)

@app.route('/AboutUs')
def about():
     msg = ''
     return render_template('AboutUs.html', msg=msg)
# http://localhost:5000/pythonlogin/ - the following will be our login page, which will use both GET and POST requests

@app.route('/EmployeePortal')
def emp():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    msg = ''
    return render_template('employee.html', msg=msg)
     
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        User = cursor.fetchone()
        # If account exists in accounts table in out database
        if User:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            #session['id'] = User['id']
            session['username'] = User['username']
            # Redirect to home page
            return redirect(url_for('home')) #need to insert url for the employee page HERE
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('loginFinal.html', msg=msg)

    # http://localhost:5000/python/logout - this will be the logout page

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'first_name' in request.form and 'last_name' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        firstName = request.form['first_name']
        lastName = request.form['last_name']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO User VALUES (%s, %s, %s, %s, Null, 1)', (username, password, firstName, lastName))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

#localhost:5003/cargo
@app.route('/cargo')
def cargo():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from Cargo")
    mysql.connection.commit()
    data = cursor.fetchall()
    cursor.close()
    print(data)
    return render_template('cargo.html', data=data)

#localhost:5003/cargo/delete
@app.route('/cargo/delete', methods = ['GET', 'POST'])
def cargo_delete():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * from Cargo")
        data = cursor.fetchall()
        print(data)
        return render_template('cargoDelete.html', data = data) #we render the table

    if request.method == 'POST' and 'cargo_ID' in request.form :
        cargo_ID = request.form['cargo_ID']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM Cargo WHERE cargo_ID = %s', (cargo_ID,))
        mysql.connection.commit()
        return redirect(url_for('cargo_delete'))

#localhost:5003/cargo/update
@app.route('/cargo/update', methods = ['GET', 'POST'])
def cargo_update():
    msg = ''
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * from Cargo")
        data = cursor.fetchall()
        print(data)
        return render_template('editCargo.html', data = data) #we render the table
    
    if request.method == 'POST' and 'cargo_ID' in request.form and 'type' in request.form and 'weight' in request.form and 'owner' in request.form and 'carno' in request.form and 'train_ID' in request.form:
        cargo_ID = request.form['cargo_ID']
        type = request.form['type']
        weight = request.form['weight']
        owner = request.form['owner']
        car_number = request.form['carno']
        train_ID = request.form['train_ID']
#        cursor = mysql.connection.cursor()
#        cursor.execute('SELECT train_length FROM Train WHERE train_ID = %s', (train_ID,))
#        mysql.connection.commit()
#        response = cursor.fetchone()
#        if car_number <= str(response):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE Cargo SET type=%s, weight=%s, owner=%s, car_number =%s, train_ID=%s WHERE cargo_ID=%s', (type,weight,owner,car_number,train_ID, cargo_ID))
        mysql.connection.commit()
        return redirect(url_for('cargo_update'))
#        else:
#            msg = 'Train length is too long, It will not be added!'
           # return render_template('editCargo.html', msg = msg)
#            return redirect(url_for('cargo_update'))
@app.route('/cargo/add', methods = ['GET', 'POST'])
def cargo_add():

    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * from Cargo")
        data = cursor.fetchall()
        print(data)
        return render_template('cargoAdd.html', data = data) #we render the table
    
    if request.method == 'POST' and 'type' in request.form and 'weight' in request.form and 'owner' in request.form and 'carno' in request.form and 'trainID' in request.form:
        type = request.form['type']
        weight = request.form['weight']
        owner = request.form['owner']
        car_number = request.form['carno']
        train_ID = request.form['trainID']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO Cargo VALUES (NULL, %s, %s, %s, %s, %s)', (type,weight,owner,car_number,train_ID))
        mysql.connection.commit()
        return redirect(url_for('cargo_add'))

#http://localhost:5003/schedule-search
@app.route('/schedule-search', methods = ['GET'])
def sched_search():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    sched_id = request.form['sched_ID']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM 'Schedule' WHERE sched_ID = %i",(sched_id,))
    schedules = cursor.fetchall()
    return render_template('schedSearch.html', schedules=schedules)
# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests


@app.route('/Route')
def RouteView():
    # Check if user is loggedin, return redirect to login page if not
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from Route")
    mysql.connection.commit()
    data = cursor.fetchall()
    cursor.close()
    print(data)
    return render_template('Route.html', data=data)

@app.route('/Route/add', methods = ['GET', 'POST'])
def route_add(): 
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * from Route")
        data = cursor.fetchall()
        print(data)
        return render_template('routeAdd.html', data = data) #we render the table
    
    if request.method == 'POST' and 'stops' in request.form:
        stops = request.form['stops']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO Route VALUES (NULL, %s)', (stops,))
        mysql.connection.commit()
        return redirect(url_for('route_add'))
    
    
@app.route('/Route/delete', methods = ['GET', 'POST'])
def route_delete(): 
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * from Route")
        data = cursor.fetchall()
        print(data)
        return render_template('routeDelete.html', data = data) #we render the table

    if request.method == 'POST' and 'route_ID' in request.form :
        route_ID = request.form['route_ID']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM Route WHERE route_ID = %s', (route_ID,))
        mysql.connection.commit()
        return redirect(url_for('route_delete'))
@app.route('/Route/update')
def route_update():
    msg = ''
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * from Route")
        data = cursor.fetchall()
        print(data)
        return render_template('routeUpdate.html', data = data) #we render the table
    
    if request.method == 'POST' and 'route_ID' in request.form and 'stops' in request.form:
        route_ID = request.form['route_ID']
        stops = request.form['stops']
        #cursor = mysql.connection.cursor()
        #cursor.execute('SELECT train_length FROM Train WHERE train_ID = %s', (train_ID,))
        #mysql.connection.commit()
        #response = cursor.fetchone()
        #if car_number <= response:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE Route SET stops=%s WHERE route_ID=%s', (stops,route_ID))
        mysql.connection.commit()
        return redirect(url_for('route_update'))
        #else:
           # msg = 'Train length is too long, It will not be added!'
            #return render_template('editCargo.html', msg = msg)
@app.route('/Schedule')
def ScheduleView():
    # Check if user is loggedin, return redirect to login page if not
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from Schedule")
    mysql.connection.commit()
    data = cursor.fetchall()
    cursor.close()
    print(data)
    return render_template('Schedule.html', data=data)

@app.route('/Schedule/add')
def schedule_add(): 
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * from Schedule")
        data = cursor.fetchall()
        print(data)
        return render_template('scheduleAdd.html', data = data) #we render the table
    
    if request.method == 'POST' and 'source' in request.form and 'destination' in request.form and 'start_time' in request.form and 'end_time' in request.form:
        source = request.form['source']
        dest = request.form['destination']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO Schedule VALUES (NULL, %s, %s, %s, %s)', (source,dest,start_time,end_time,))
        mysql.connection.commit()
        return redirect(url_for('schedule_add'))
@app.route('/Schedule/delete')
def schedule_delete():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * from Route")
        data = cursor.fetchall()
        print(data)
        return render_template('scheduleDelete.html', data = data) #we render the table

    if request.method == 'POST' and 'sched_ID' in request.form :
        sched_ID = request.form['sched_ID']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM Route WHERE sched_ID = %s', (sched_ID,))
        mysql.connection.commit()
        return redirect(url_for('schedule_delete'))
@app.route('/Schedule/update')
def schedule_update():
    msg = ''
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * from Schedule")
        data = cursor.fetchall()
        print(data)
        return render_template('editSchedule.html', data = data) #we render the table
    
    if request.method == 'POST' and 'sched_ID' in request.form and 'source' in request.form and 'destination' in request.form and 'start_time' in request.form and 'end_time' in request.form:
        sched_ID = request.form['sched_ID']
        source = request.form['source']
        dest = request.form['destination']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        # cursor = mysql.connection.cursor()
        # cursor.execute('SELECT train_length FROM Train WHERE train_ID = %s', (train_ID,))
        # mysql.connection.commit()
        # response = cursor.fetchone()
        #if car_number <= response:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE SChedule SET source=%s, dest=%s, start_time=%s, end_time=%s WHERE sched_ID=%s', (source,dest,start_time,end_time,sched_ID))
        mysql.connection.commit()
        return redirect(url_for('schedule_update'))
        #else:
           # msg = 'Train length is too long, It will not be added!'
           # return render_template('editCargo.html', msg = msg)
@app.route('/Station')
def StationView():
    # Check if user is loggedin, return redirect to login page if not
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from Station")
    mysql.connection.commit()
    data = cursor.fetchall()
    cursor.close()
    print(data)
    return render_template('Station.html', data=data)

@app.route('/Station/add')
def station_add():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * from Station")
        data = cursor.fetchall()
        print(data)
        return render_template('stationAdd.html', data = data) #we render the table
    
    if request.method == 'POST' and 'name' in request.form and 'location' in request.form:
        name = request.form['name']
        location = request.form['location']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO Station VALUES (NULL, %s, %s)', (name,location,))
        mysql.connection.commit()
        return redirect(url_for('station_add'))
    
@app.route('/Station/delete')
def station_delete():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * from Station")
        data = cursor.fetchall()
        print(data)
        return render_template('stationDelete.html', data = data) #we render the table

    if request.method == 'POST' and 'station_ID' in request.form :
        station_ID = request.form['station_ID']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM Station WHERE station_ID = %s', (station_ID,))
        mysql.connection.commit()
        return redirect(url_for('station_delete'))
@app.route('/Station/update')
def station_update():
    #msg = ''
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * from Station")
        data = cursor.fetchall()
        print(data)
        return render_template('editStation.html', data = data) #we render the table
    
    if request.method == 'POST' and 'station_ID' in request.form and 'name' in request.form and 'location' in request.form:
        station_ID = request.form['station_ID']
        name = request.form['name']
        location = request.form['location']
        cursor = mysql.connection.cursor()
        #cursor.execute('SELECT train_length FROM Train WHERE train_ID = %s', (train_ID,))
        #mysql.connection.commit()
        #response = cursor.fetchone()
        #if car_number <= response:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE Station SET name=%s, location=%s WHERE station_ID=%s', (name,location,station_ID))
        mysql.connection.commit()
        return redirect(url_for('station_update'))
        #else:
           # msg = 'Train length is too long, It will not be added!'
            #return render_template('editCargo.html', msg = msg)

@app.route('/Track')
def TrackView():
    # Check if user is loggedin, return redirect to login page if not
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from Track")
    mysql.connection.commit()
    data = cursor.fetchall()
    cursor.close()
    print(data)
    return render_template('Track.html', data=data)

@app.route('/Track/add')
def track_add():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * from Track")
        data = cursor.fetchall()
        print(data)
        return render_template('trackAdd.html', data = data) #we render the table
    
    if request.method == 'POST' and 'direction' in request.form:
        direction = request.form['direction']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO Track VALUES (NULL, %s)', (direction,))
        mysql.connection.commit()
        return redirect(url_for('track_add'))

@app.route('/Track/delete')
def track_delete():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * from Track")
        data = cursor.fetchall()
        print(data)
        return render_template('trackDelete.html', data = data) #we render the table

    if request.method == 'POST' and 'track_ID' in request.form :
        track_ID = request.form['track_ID']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM Track WHERE track_ID = %s', (track_ID,))
        mysql.connection.commit()
        return redirect(url_for('track_delete'))

@app.route('/Track/update')
def track_update():
    msg = ''
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * from Track")
        data = cursor.fetchall()
        print(data)
        return render_template('editTrack.html', data = data) #we render the table
    
    if request.method == 'POST' and 'track_ID' in request.form and 'direction' in request.form:
        track_ID = request.form['track_ID']
        direction = request.form['direction']
        cursor = mysql.connection.cursor()
        #cursor.execute('SELECT train_length FROM Train WHERE train_ID = %s', (train_ID,))
        #mysql.connection.commit()
        #response = cursor.fetchone()
        #if car_number <= response:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE Track SET direction=%s WHERE track_ID=%s', (direction,track_ID))
        mysql.connection.commit()
        return redirect(url_for('track_update'))
        #else:
            #msg = 'Train length is too long, It will not be added!'
            #return render_template('trackUpdate.html', msg = msg)

@app.route('/Train')
def TrainView():
    # Check if user is loggedin, return redirect to login page if not
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from Train")
    mysql.connection.commit()
    data = cursor.fetchall()
    cursor.close()
    print(data)
    return render_template('Train.html', data=data)

@app.route('/Train/add')
def train_add():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * from Train")
        data = cursor.fetchall()
        print(data)
        return render_template('trainAdd.html', data = data) #we render the table
    
    if request.method == 'POST' and 'train_length' in request.form and 'route_ID' in request.form and 'sched_ID' in request.form:
        length = request.form['train_length']
        route_ID = request.form['route_ID']
        sched_ID = request.form['sched_ID']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO Train VALUES (NULL, %s, %s, %s)', (length,route_ID,sched_ID,))
        mysql.connection.commit()
        return redirect(url_for('train_add'))

@app.route('/Train/delete')
def train_delte():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * from Train")
        data = cursor.fetchall()
        print(data)
        return render_template('trainDelete.html', data = data) #we render the table

    if request.method == 'POST' and 'train_ID' in request.form :
        train_ID = request.form['train_ID']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM Train WHERE train_ID = %s', (train_ID,))
        mysql.connection.commit()
        return redirect(url_for('train_delete'))

@app.route('/Train/update')
def train_update():
    #msg = ''
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * from Train")
        data = cursor.fetchall()
        print(data)
        return render_template('editTrain.html', data = data) #we render the table
    
    if request.method == 'POST' and 'train_ID' in request.form and 'train_length' in request.form and 'route_ID' in request.form and 'sched_ID' in request.form:
        train_ID = request.form['train_ID']
        length = request.form['train_length']
        route_ID = request.form['route_ID']
        sched_ID = request.form['sched_ID']
        cursor = mysql.connection.cursor()
        #cursor.execute('SELECT train_length FROM Train WHERE train_ID = %s', (train_ID,))
        #mysql.connection.commit()
        #response = cursor.fetchone()
        #if car_number <= response:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE Station SET train_length=%s, route_ID=%s, sched_ID=%s WHERE train_ID=%s', (length,route_ID,sched_ID,train_ID))
        mysql.connection.commit()
        return redirect(url_for('train_update'))
        #else:
           # msg = 'Train length is too long, It will not be added!'
            #return render_template('editCargo.html', msg = msg)
#run the application
app.run(host='localhost', port=5003)
