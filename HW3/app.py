from flask import *

app = Flask(__name__)

@app.route('/')
def register():
    return render_template('register.html')

@app.route('/output', methods=['POST'])
def output():
    lastname = request.form['lastname']
    firstname = request.form['firstname']
    sex = request.form['sex']
    institution = request.form['institution']
    email = request.form['email']

    return render_template('output.html' ,lastname = lastname ,firstname = firstname ,sex = sex ,institution = institution ,email = email)

if __name__ == '__main__':
    app.run(debug=True)
