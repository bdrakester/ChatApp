from flask import Flask, render_template, request, make_response, session
from flask import redirect, url_for
from flask_socketio import SocketIO, emit, join_room
from database import ChatAppDB
from datetime import datetime

app = Flask(__name__)
chatAppDB = ChatAppDB()
COOKIE_NAME = "ChatAppSession"
app.secret_key = "insecurekey"
socketio = SocketIO(app)

@app.route("/")
def index():
	if "id" in session:
		return redirect(url_for('lobby'))
	else:
		return redirect(url_for('login'))

@app.route("/users")
def users():
	userList = chatAppDB.get_all_usernames()
	return render_template("users.html", users = userList)

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		username = request.form.get("username")

		if not chatAppDB.username_exists(username):
			chatAppDB.create_user(username,'password',username)

		session["id"] = chatAppDB.create_session(username)
		#session.permanent = True
		return redirect(url_for('lobby'))
	else:
		return render_template("login.html")

@app.route("/lobby", methods=["GET", "POST"])
def lobby():
	if not "id" in session:
		return redirect(url_for('login'))

	username = chatAppDB.get_session_username(session["id"])

	if request.method == "POST":
		newChatroom = request.form.get("chatroom")
		if not chatAppDB.chatroom_exists(newChatroom):
			chatAppDB.create_chatroom(newChatroom)

	chatrooms = chatAppDB.get_all_chatrooms()

	return render_template("lobby.html", username = username, chatrooms = chatrooms)

@app.route("/chatroom/<string:chatroom_name>")
def chatroom(chatroom_name):
	if not "id" in session:
		return redirect(url_for('login'))

	if not chatAppDB.chatroom_exists(chatroom_name):
		return render_template("error.html", message="Chatroom does not exist.")

	username = chatAppDB.get_session_username(session["id"])
	prev_messages = chatAppDB.get_messages(chatroom_name, 10)
	return render_template("chatroom.html", name=chatroom_name, messages=prev_messages)

@socketio.on("join")
def join(data):
	chatroom = data["chatroom"]
	join_room(chatroom)
	username = chatAppDB.get_session_username(session["id"])
	#now = datetime.now().replace(microsecond=0).isoformat(' ')
	#message = f"{username} has joined the room."
	#chatAppDB.add_message(chatroom, username, message, now)
	#emit("receive message", {"username": '', "time": now, "message": message}, room=chatroom)

@socketio.on("send message")
def send_message(data):
	message = data["message"]
	chatroom = data["chatroom"]
	username = chatAppDB.get_session_username(session["id"])
	now = datetime.now().replace(microsecond=0).isoformat(' ')
	chatAppDB.add_message(chatroom, username, message, now)
	emit("receive message", {"username": username, "time": now, "message": message}, room=chatroom)
