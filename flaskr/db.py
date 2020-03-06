#db.py
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))

    """Add Sample Data to db"""
    sample_data()

def sample_data():
    db = get_db()

    """Generate Teacher"""
    db.execute(
    'INSERT INTO user (username, password) VALUES (?, ?)',
    ("test@nimbleknow.com", generate_password_hash("123"))
    )
    db.commit()
    # if db.execute(
    #         'SELECT id FROM user WHERE username = ?', ("test@nimbleknow.com",)).fetchone() is not None:
    #         print("works")
    """Generate Classroom"""
    db.execute(
    'INSERT INTO classroom (classname, teacher, password) VALUES (?, ?, ?)',
    ("123", "test@nimbleknow.com", generate_password_hash("123"))
    )
    db.commit()

    """Generate Question"""
    db.execute(
    'INSERT INTO question (author_id, q_type, classname, content) VALUES (?, ?, ?, ?)',
    (1, "multichoice", "123", "What is your favorite letter?")
    )
    db.commit()



    """Adding the data for each choice to db"""
    db.execute(
    'INSERT INTO options (question_id, label, content, numChosen) VALUES (?, ?, ?, ?)',
    (1, "a", "option a", 10)
    )
    db.commit()

    db.execute(
    'INSERT INTO options (question_id, label, content, numChosen) VALUES (?, ?, ?, ?)',
    (1, "b", "option b", 6)
    )
    db.commit()

    db.execute(
    'INSERT INTO options (question_id, label, content, numChosen) VALUES (?, ?, ?, ?)',
    (1, "c", "option c", 8)
    )
    db.commit()

    db.execute(
    'INSERT INTO options (question_id, label, content, numChosen) VALUES (?, ?, ?, ?)',
    (1, "d", "option d", 22)
    )
    db.commit()

@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
