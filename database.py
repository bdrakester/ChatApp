#!/usr/local/bin/python3

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from getpass import getpass
from uuid import uuid4

class ChatAppDB:
    """
    Database interface
    """

    def __init__(self):
        connString = "postgresql://chatappdbuser:chatappdbuser@127.0.0.1:5432/chatapp"
        self.engine = create_engine(connString)
        self.db = scoped_session(sessionmaker(bind=self.engine))

    def create_user(self, username, password, display_name):
        self.db.execute("INSERT INTO users (username, password, display_name) \
                        VALUES (:username, :password, :display_name)",
                        {"username": username, "password": password, "display_name": display_name})
        self.db.commit()

    def print_users(self):
        sqlCommand = "SELECT * FROM users"
        names = self.db.execute(sqlCommand).fetchall()

        print("Users : ")
        for name in names:
            print(' ' * 4 + name.display_name + '  |   ' + name.username + '  |  ' + name.password)

    def username_exists(self, username):
        sqlCommand = f"SELECT COUNT(username) FROM users WHERE username = '{username}'"

        if self.db.execute(sqlCommand).fetchone()[0] > 0:
            return True
        else:
            return False

    def get_all_usernames(self):
        sqlCommand = "SELECT username FROM users"
        sqlResult = self.db.execute(sqlCommand).fetchall()

        usernames = []

        for user in sqlResult:
            usernames.append(user.username)

        return usernames

    def get_user_id(self, username):
        user_id = self.db.execute("SELECT id FROM users WHERE username = :username",
                                {"username": username}).fetchone()[0]
        return user_id

    def create_session(self, username):
        session_id = str(uuid4())
        user_id = self.get_user_id(username)

        self.db.execute("INSERT INTO sessions (id, user_id) VALUES (:id, :user_id)",
                        {"id": session_id, "user_id": user_id})
        self.db.commit()

        return session_id

    def get_session_username(self, session_id):
        username = self.db.execute("SELECT username FROM users JOIN sessions \
                                    ON sessions.user_id = users.id WHERE sessions.id = :id",
                                     {"id": session_id}).fetchone()[0]
        return username

    def get_all_chatrooms(self):
        sqlResult = self.db.execute("SELECT name FROM chatrooms").fetchall()

        chatrooms = []
        for chatroom in sqlResult:
            chatrooms.append(chatroom.name)

        return chatrooms

    def create_chatroom(self, name):

        self.db.execute("INSERT INTO chatrooms (name) VALUES (:name)", {"name": name})
        self.db.commit()

    def chatroom_exists(self,name):
        if self.db.execute("SELECT COUNT (name) FROM chatrooms WHERE name = :name",
                        {"name": name}).fetchone()[0] > 0:
            return True
        else:
            return False

    def get_chatroom_id(self, name):
        chatroom_id = self.db.execute("SELECT id FROM chatrooms WHERE name = :name",
                                {"name": name}).fetchone()[0]
        return chatroom_id

    #def join_chatroom(chatroom, username):

    def add_message(self, chatroom, username, message, sent_time):
        user_id = self.get_user_id(username)
        chatroom_id = self.get_chatroom_id(chatroom)
        self.db.execute("INSERT INTO messages (chatroom_id, message, user_id, sent_time) \
            VALUES (:chatroom_id, :message, :user_id, :sent_time)",
            {"chatroom_id": chatroom_id, "message": message, "user_id": user_id, "sent_time": sent_time})

        self.db.commit()

    def add_anon_message(self, chatroom, message, sent_time):
        chatroom_id = self.get_chatroom_id(chatroom)

    def get_messages(self, chatroom, amount):
        """
        Return a list of  message dictionaries.  Message dictionary contains
        'time', 'username' and 'text' fields.
        """
        chatroom_id = self.get_chatroom_id(chatroom)
        sqlResult =self.db.execute("SELECT sent_time, username, message \
            FROM messages JOIN users ON users.id = messages.user_id \
            WHERE messages.chatroom_id = (:chatroom_id) \
            ORDER BY sent_time LIMIT (:amount)",
            {"chatroom_id": chatroom_id, "amount": amount}).fetchall()

        messages = []
        for message in sqlResult:
            messageDict = {"time": message.sent_time.isoformat(' '), "username": message.username, "text": message.message}
            messages.append(messageDict)

        return messages

def main():
    #engine = create_engine('postgresql://chatappdbuser:chatappdbuser@127.0.0.1:5432/chatapp')
    #db = scoped_session(sessionmaker(bind=engine))

    print("Hello SQL Alchemy")
    chatAppDB = ChatAppDB()
    chatAppDB.print_users()

    username = input("Username: ")
    password = getpass("Password: ")

    if not (chatAppDB.username_exists(username)):
        print(f"Username {username} does not exist")
        return False

    print(f"Welcome {username}\n\n")

    testMessages = chatAppDB.get_messages("Room1",5)

    print(testMessages)

if __name__ == "__main__":
    main()
