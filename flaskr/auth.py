#auth.py
import functools

from flask import Flask, render_template, make_response, Blueprint, redirect, url_for, flash, request, session, g
from werkzeug.security import check_password_hash, generate_password_hash


from flaskr.db import get_db



bp = Blueprint('auth', __name__)
@bp.route('/teacherlogin')
def teacherlogin():
    return render_template('auth/teacherlogin.html')



@bp.route('/studentlogin', methods=('GET', 'POST'))
def studentlogin():
    if request.method == 'POST':
        classname = request.form.get("classname")
        password = request.form.get("password")
        db = get_db()
        error = None
        classroom = db.execute(
         "SELECT * FROM classroom WHERE classname = ?", (classname,)
        ).fetchone()

        if classroom is None:
            error = 'Incorrect classname.'
        elif not check_password_hash(classroom["password"], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['classroom_id'] = classroom['id']
            return redirect(url_for('review.question'))

        flash(error)
    return render_template('auth/studentlogin.html')

@bp.route('/registerclass', methods=('GET', 'POST'))
def registerclass():
    if request.method == 'POST':
        classname = request.form['classname']
        password = request.form['password']
        db = get_db()
        error = None
        if not classname:
            error = 'Class Name is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM classroom WHERE classname = ?', (classname,)).fetchone() is not None:
            error = 'Class {} is already registered.'.format(classname)
        if error is None:
            db.execute(
            'INSERT INTO classroom (classname, password) VALUES (?, ?)',
            (classname, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('review.question'))
        flash(error)
    return render_template('auth/registerclass.html')
@bp.route('/register', methods=('GET', 'POST'))
def register():
  # many cases
  if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)
        if error is None:
            db.execute(
            'INSERT INTO user (username, password) VALUES (?, ?)',
            (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.teacherlogin'))
        flash(error)
  return render_template('auth/register.html')