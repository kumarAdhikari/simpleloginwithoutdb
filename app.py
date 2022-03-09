from flask import Flask, redirect, url_for, render_template, request, session
from flask_socketio import SocketIO, join_room,leave_room,emit
from flask_session import Session

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'
socketio = SocketIO(app)

Session(app)
Socketio = SocketIO(app, manage_session=False)
socketio.init_app(app, cors_allowed_origins="*")
ep = {"kumar": "python"}

@app.route('/', methods=['POST', 'GET'])
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
        ep[username] = password
    return render_template('register.html', name=firstName, username = username, password = password)


@app.route('/loginpage',methods=['POST', 'GET'])
def loginpage():
    if request.method == 'POST':
        return render_template('login.html')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if(request.method=='POST'):
        username = request.form['username']
        room = request.form['room']
        password = request.form['password']
        #Store the data in session
        session['username'] = username
        session['room'] = room
        if username in ep and ep[username] == password:
            return render_template('chat.html', session = session)
        else:
            return render_template('loginresult.html')
    else:
        if(session.get('username') is not None):
            return render_template('chat.html', session = session)
        else:
            return redirect(url_for('index'))


@socketio.on('join', namespace='/chat')
def join(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room=room)


if __name__ == '__main__':
    socketio.run(app, cors_allowed_origins="*")
