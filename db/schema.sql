CREATE TABLE chatrooms (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    display_name VARCHAR NOT NULL,
    chatroom_id INTEGER REFERENCES chatrooms
);

CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    user_id INTEGER REFERENCES users
);

CREATE TABLE messages (
  id SERIAL PRIMARY KEY,
  message VARCHAR NOT NULL,
  chatroom_id INTEGER REFERENCES chatrooms,
  user_id INTEGER REFERENCES users,
  sent_time TIMESTAMP
)
