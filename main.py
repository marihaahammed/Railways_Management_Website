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

# http://localhost:5000/pythonlogin/ - the following will be our login page, which will use both GET and POST requests
@app.route('/pythonlogin/', methods=['GET', 'POST'])
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
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('railways.html', msg=msg)

    # http://localhost:5000/python/logout - this will be the logout page

@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/cargo', methods = ['GET', 'POST', 'UPDATE', 'DELETE'])
def cargo():
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

@app.route('/cargo/delete', methods = ['POST'])
def cargo_delete():
                type = request.form['type']
                weight = request.form['weight']
                owner = request.form['owner']
                car_number = request.form['car_number']
                train_ID = request.form['train_ID']
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("DELETE FROM 'Cargo' WHERE train_ID = %i", (train_ID))

@app.route('/cargo/update', methods = ['UPDATE'])
def cargo_update():
                type = request.form['type']
                weight = request.form['weight']
                owner = request.form['owner']
                car_number = request.form['car_number']
                train_ID = request.form['train_ID']
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("UPDATE 'Cargo' SET type=%i, weight=%i, owner=%s, car_number =%i, train_ID=%i where train_ID=%i", (type,weight,owner,car_number,train_ID, tr>
      
# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
#@app.route('/pythonlogin/register', methods=['GET', 'POST'])
#def register():
    # Output message if something goes wrong...
 #   msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
  #  if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
   #     username = request.form['username']
    #    password = request.form['password']
     #   email = request.form['email']
        # Check if account exists using MySQL
      #  cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       # cursor.execute('SELECT * FROM User WHERE username = %s', (username,))
        #account = cursor.fetchone()
        # If account exists show error and validation checks
        #if account:
        #    msg = 'Account already exists!'
        #elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        #    msg = 'Invalid email address!'
        #elif not re.match(r'[A-Za-z0-9]+', username):
        #    msg = 'Username must contain only characters and numbers!'
        #elif not username or not password or not email:
        #    msg = 'Please fill out the form!'
        #else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
         #   cursor.execute('INSERT INTO User VALUES (NULL, %s, %s, %s)', (username, password, email,))
          #  mysql.connection.commit()
           # msg = 'You have successfully registered!'
    #elif request.method == 'POST':
        # Form is empty... (no POST data)
     #   msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    #return render_template('register.html', msg=msg)

# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/pythonlogin/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/pythonlogin/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/searchform')
def searchform():
    # Check if user is loggedin, return redirect to login page if not
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('form.html', username=session['username'])


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
app.run(host='localhost', port=5000)
