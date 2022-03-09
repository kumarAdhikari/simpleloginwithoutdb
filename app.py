from flask import Flask,redirect,url_for,render_template,request

app = Flask(__name__)


@app.route('/')
def homepage():  # put application's code here
    return render_template('index.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        return render_template("signup.html")


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
    return render_template('register.html', name=firstName, username = username, password = password)


@app.route('/loginpage',methods=['POST', 'GET'])
def loginpage():
    if request.method == 'POST':
        return render_template('login.html')


@app.route('/loginpost', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        loginusername = request.form['username']
        loginpassword = request.form['password']
        return render_template('loginresult.html', loginusername=loginusername, loginpassword=loginpassword)


if __name__ == '__main__':
    app.run()
