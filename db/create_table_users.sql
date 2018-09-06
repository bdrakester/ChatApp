CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    display_name VARCHAR NOT NULL,
    chatroom_id INTEGER REFERENCES chatrooms
);
