DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS info CASCADE;
DROP TABLE IF EXISTS areas CASCADE;
DROP TABLE IF EXISTS threads CASCADE;
DROP TABLE IF EXISTS area_access CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    admin BOOLEAN,
    visibility BOOLEAN
);

CREATE TABLE areas (
    id SERIAL PRIMARY KEY,
    area_name TEXT,
    visibility BOOLEAN
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    thread_name TEXT,
    area_id INTEGER REFERENCES areas,
    visibility BOOLEAN
);

CREATE TABLE info (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP,
    thread_id INTEGER REFERENCES threads,
    thread_message BOOLEAN,
    visibility BOOLEAN
);

CREATE TABLE area_access (
    id SERIAL PRIMARY KEY,
    area_id INTEGER REFERENCES areas,
    user_id INTEGER REFERENCES users,
    visibility BOOLEAN
);


INSERT INTO areas (area_name, visibility) VALUES ('Alue1', TRUE);
INSERT INTO areas (area_name, visibility) VALUES ('Alue2', TRUE);