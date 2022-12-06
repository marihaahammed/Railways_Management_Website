from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
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
        cursor.execute('SELECT * FROM Users WHERE username = %s', (username,))
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
            cursor.execute('INSERT INTO Users VALUES (%s, %s, %s, %s, Null, 1)', (username, password, firstName, lastName))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

#@app.route('/home')
#def home():
    # Check if user is loggedin
   # if 'loggedin' in session:
        # User is loggedin show them the home page
    #    return render_template('railways.html', username=session['username'])
    # User is not loggedin redirect to login page
   # return redirect(url_for('login'))



#localhost:5003/cargo
@app.route('/cargo', methods = ['GET', 'POST'])
def cargo():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        type = request.form['type']
        weight = request.form['weight']
        owner = request.form['owner']
        car_number = request.form['car_number']
        train_ID = request.form['train_ID']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO 'Cargo' (type,weight,owner,car_number,train_ID) values (%i, %i, %s, %i, %i)", (type,weight,owner,car_number,train_ID))

    elif request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM 'Cargo'")
        cargos = cursor.fetchall()
        return render_template('cargo.html', cargos=cargos)

#localhost:5003/cargo/delete
@app.route('/cargo/delete', methods = ['POST'])
def cargo_delete():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    type = request.form['type']
    weight = request.form['weight']
    owner = request.form['owner']
    car_number = request.form['car_number']
    train_ID = request.form['train_ID']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM 'Cargo' WHERE train_ID = %i", (train_ID))

#localhost:5003/cargo/update
@app.route('/cargo/update', methods = ['GET', 'POST'])
def cargo_update():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        cargo_ID = request.arg['cargo_ID']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM 'Cargo' WHERE cargo_ID = %i", (cargo_ID))
        cargo = cursor.fetchone()
        return render_template('editCargo.html', cargo=cargo)
    elif request.method == 'POST':
                type = request.form['type']
                weight = request.form['weight']
                owner = request.form['owner']
                car_number = request.form['car_number']
                train_ID = request.form['train_ID']
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("UPDATE 'Cargo' SET type=%i, weight=%i, owner=%s, car_number =%i, train_ID=%i where train_ID=%i", (type,weight,owner,car_number,train_ID, train_ID))

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


@app.route('/search', methods = ['POST', 'GET'])
def search():
    # Check if user is loggedin, return redirect to login page if not
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return "Fill out the Search Form"
     
    if request.method == 'POST':
        name = request.form['name']
        id = request.form['id']
        cursor = mysql.connection.cursor()
        if name:
            cursor.execute("SELECT * from instructor where name = %s",[name])
        if id:
            cursor.execute("SELECT * from instructor where ID = %s",[id])
        mysql.connection.commit()
        data = cursor.fetchall()
        cursor.close()
        print(data)
        #return f"Done!! Query Result is {data}"
        return render_template('results.html', data=data)



#run the application
app.run(host='localhost', port=5003)
