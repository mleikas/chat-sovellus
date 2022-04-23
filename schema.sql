CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    visibility BOOLEAN
);

CREATE TABLE info (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP,
    thread_id INTEGER REFERENCES threads,
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

CREATE TABLE area_access (
    area_id INTEGER REFERENCES areas,
    visibility BOOLEAN
);

INSERT INTO areas (area_name, visibility) VALUES ('Alue1', TRUE);
INSERT INTO areas (area_name, visibility) VALUES ('Alue2', TRUE);