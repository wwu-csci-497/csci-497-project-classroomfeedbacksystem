DROP TABLE IF EXISTS user;
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

DROP TABLE IF EXISTS classroom;
CREATE TABLE classroom (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  classname TEXT UNIQUE NOT NULL,
  teacher TEXT NOT NULL,
  password TEXT NOT NULL,
  FOREIGN KEY (teacher) REFERENCES user (id)
);

DROP TABLE IF EXISTS question;
CREATE TABLE question (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  author_id INTEGER NOT NULL,
  q_type TEXT NOT NULL,
  classname TEXT NOT NULL,
  content TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);


DROP TABLE IF EXISTS options;
CREATE TABLE options(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  question_id INTEGER NOT NULL,
  label TEXT,
  content TEXT,
  FOREIGN KEY (question_id) REFERENCES question (id)
);

DROP TABLE IF EXISTS response;
CREATE TABLE response (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  content TEXT,
  choice TEXT,
  question_id INTEGER NOT NULL,
  FOREIGN KEY (question_id) REFERENCES question (id)
);

