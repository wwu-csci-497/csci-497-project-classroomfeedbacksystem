#auth.py
from flask import Flask, render_template, make_response, Blueprint, redirect, url_for, flash, request
from werkzeug.security import check_password_hash, generate_password_hash


from flaskr.db import get_db

# import more
bp = Blueprint('auth', __name__)
@bp.route('/teacherlogin')
def teacherlogin():
    return render_template('auth/teacherlogin.html')
@bp.route('/studentlogin')
def studentlogin():
    return render_template('auth/studentlogin.html')
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