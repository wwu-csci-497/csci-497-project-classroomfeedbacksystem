#review.py
from flask import Flask, render_template, make_response, Blueprint, g, request, redirect, url_for, flash

from flaskr.auth import login_required , class_required
from flaskr.db import get_db

# import more
bp = Blueprint('review', __name__)

@bp.route('/')
def home():
    db = get_db()
    questions = db.execute(
        'SELECT r.id, created, author_id, content, username'
        ' FROM question r JOIN user u ON r.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('review/home.html', questions=questions)

# @bp.route('/question')
# def question():
#     return render_template('review/question.html')

@bp.route('/about')
def about():
    return render_template('review/about.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    classrooms = db.execute(
        'SELECT c.id, created, classname'
        ' FROM classroom c JOIN user u ON c.teacher = u.id'
        ' WHERE teacher = ?'
        ' ORDER BY created DESC',
        (g.user['id'],)
    ).fetchall()
    return render_template('review/dashboard.html', classrooms=classrooms)


@bp.route("/<classname>/classroom")
@login_required
def classroom(classname):
    db = get_db()
    questions = db.execute(
        'SELECT id, content, classname, created'
        ' FROM question' #r JOIN user u ON c.teacher = r.id'
        ' WHERE classname = ?'
        ' ORDER BY created DESC',
        (classname,)
    ).fetchall()
    print(classname)
    return render_template('review/classroom.html', questions = questions)

@bp.route("/<classname>/studentclassroom")
@class_required
def studentclassroom(classname):
    db = get_db()
    questions = db.execute(
        'SELECT id, content, classname, created'
        ' FROM question' #r JOIN user u ON c.teacher = r.id'
        ' WHERE classname = ?'
        ' ORDER BY created DESC',
        (classname,)
    ).fetchall()
    print(classname)
    return render_template('review/studentclassroom.html', questions = questions)


@bp.route("/<question_id>/<classname>/responses")
@login_required
def responses(question_id, classname):
    db = get_db()
    responses = db.execute(
        'SELECT id, content, created, question_id'
        ' FROM response' #r JOIN user u ON c.teacher = r.id'
        ' WHERE question_id = ?'
        ' ORDER BY created DESC',
        (question_id,)
    ).fetchall()
    question = db.execute(
        'SELECT content'
        ' FROM question' 
        ' WHERE id = ?',
        (question_id,)
    ).fetchone()
    return render_template('review/responses.html', responses = responses, question = question)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        text = request.form['question-text']
        text = text.strip()
        classname = request.form['class']
        classname = classname.strip()
        db = get_db()
        error = None
        if not text:
            error = 'You didn\'t add any new question.'
        if error is None:
            db.execute(
            'INSERT INTO question (author_id, content, classname) VALUES (?, ?, ?)',   
            (g.user['id'], text, classname)
            )
            db.commit()
            print(classname)
            return redirect(url_for('review.classroom', classname = classname))
        flash(error)
    return render_template('review/create.html')

@bp.route('/<question_id>/<classname>/response', methods=('GET', 'POST'))
@class_required
def response(question_id, classname):
    db = get_db()
    question = db.execute(
        'SELECT content FROM question WHERE id = ?',   
        (question_id)
        )
    if request.method == 'POST':
        text = request.form['response-text']
        text = text.strip()
        error = None
        if not text:
            error = 'You didn\'t add any new response.'
        if error is None:
            db.execute(
            'INSERT INTO response (content, question_id) VALUES (?, ?)',   
            (text, question_id)
            )
            db.commit()
            return redirect(url_for('review.studentclassroom', classname = classname,))
        flash(error)
    
    return render_template('review/response.html', question = question )


@bp.route('/<page_name>')
def other_page(page_name):
    response = make_response(render_template('review/404.html'), 404)
    return response
if __name__ == '__main__':
    app.run(debug=True)