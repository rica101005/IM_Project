from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
app = Flask(__name__)

app.secret_key = 'secretkey' 

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"  
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "gregoriodb" 
app.config["MYSQL_CURSORCLASS"] = "DictCursor" 

mysql = MySQL(app)

@app.route("/", methods=['GET', 'POST'])
def login():
    if 'loggedin' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM Account WHERE username = %s", (username,))
        account = cur.fetchone()
        cur.close()

        if account and account['password'] == password: 
            session['loggedin'] = True
            session['acctno'] = account['acctno']
            session['username'] = account['username']
            session['role'] = account['role'] 
            session['name'] = account['name'] 

            flash(f"Welcome back, {session['name']}!", 'success')
            
            return redirect(url_for('home'))
        else:
            flash('Invalid login credentials (username and/or password)!', 'error')
            return redirect(url_for('login'))

    return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        full_name = request.form['full_name']
        sex = request.form['sex']
        dob = request.form['dob']
        username = request.form['username']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Account WHERE username = %s", (username,))
        existing_user = cur.fetchone()
        
        if existing_user:
            flash(f"Username '{username}' is already taken. Try another.", 'error')
            cur.close()
            return redirect(url_for('register'))
            
        sql = "INSERT INTO Account (name, sex, dob, username, password) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(sql, (full_name, sex, dob, username, password))
        mysql.connection.commit()
        cur.close()

        flash('Account successfully created! You can now log in.', 'success')

        return redirect(url_for('login'))
        
    return render_template("register.html")

@app.route("/home")
def home():

    if 'loggedin' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))

    user_details = None
    list_of_users = None
    
    if session['role'] == 'ordinary':

        user_details = {
            'full_name': session.get('name'),
            'sex': session.get('sex', 'N/A'), 
            'dob': session.get('dob', 'N/A'),
            'username': session.get('username'),
            'password': '********'
        }
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT name, sex, dob, username FROM Account WHERE acctno = %s", (session['acctno'],))
        db_user_details = cur.fetchone()
        cur.close()

        if db_user_details:
             user_details['full_name'] = db_user_details['name']
             user_details['sex'] = db_user_details['sex']
             user_details['dob'] = str(db_user_details['dob'])

    elif session['role'] == 'admin':
        cur = mysql.connection.cursor()

        cur.execute("SELECT acctno, name AS 'Full Name', sex, dob, username, password FROM Account")
        list_of_users = cur.fetchall()
        cur.close()

    return render_template("home.html", user_details=user_details, list_of_users=list_of_users)

@app.route("/logout")
def logout():

    session.pop('loggedin', None)
    session.pop('acctno', None)
    session.pop('username', None)
    session.pop('role', None)
    session.pop('name', None)
    
    flash('You have been successfully logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)