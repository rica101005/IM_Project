from flask import Flask, render_template, url_for, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def home():
    cur = mysql.connection.cursor()
    sql = "SELECT * FROM student"
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    return render_template('index.html', students=result, message=request.args.get("msg"))

@app.route('/addForm')
def add_form():
    return render_template('add.html')

@app.route('/addStudent', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        sex = request.form['sex']
        dept = request.form['dept']
        cur = mysql.connection.cursor()
        sql = "INSERT INTO student(name, sex, department) VALUES(%s, %s, %s)"
        cur.execute(sql, (name, sex, dept))
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('home', msg="Student Added Successfully!"))

@app.route('/deleteStudent/<int:student_id>')
def delete(student_id):
    cur = mysql.connection.cursor()
    sql = "DELETE FROM student WHERE student_id=%s"
    cur.execute(sql, (student_id, ))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('home', msg="Student Deleted Successfully!"))

@app.route('/editForm/<int:student_id>')
def edit_form(student_id):
    cur = mysql.connection.cursor()
    sql = "SELECT * FROM student WHERE student_id=%s"
    cur.execute(sql, (student_id, ))
    student = cur.fetchone()
    cur.close()
    return render_template('edit.html', student=student)

@app.route('/editStudent/<int:student_id>', methods=['POST', 'GET'])
def edit_student(student_id):
    if request.method == 'POST':
        name = request.form['name']
        sex = request.form['sex']
        dept = request.form['dept']
        cur = mysql.connection.cursor()
        sql = "UPDATE student SET name=%s, sex=%s, department=%s WHERE student_id=%s"
        cur.execute(sql, (name, sex, dept, student_id))
        mysql.connection.commit()
        cur.close()
    return redirect(url_for('home', msg="Student Updated Successfully!"))

if __name__ == '__main__':
    app.run(debug=True)