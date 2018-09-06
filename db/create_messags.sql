CREATE TABLE messages (
  id SERIAL PRIMARY KEY,
  message VARCHAR NOT NULL,
  chatroom_id INTEGER REFERENCES chatrooms,
  user_id INTEGER REFERENCES users,
  sent_time TIMESTAMP
)
