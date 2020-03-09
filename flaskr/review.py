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
        'SELECT id, content, q_type, classname, created'
        ' FROM question' #r JOIN user u ON c.teacher = r.id'
        ' WHERE classname = ?'
        ' ORDER BY created DESC',
        (classname,)
    ).fetchall()
    print(classname)
    return render_template('review/studentclassroom.html', questions = questions)


@bp.route("/<question_id>/<classname>/responses", methods=('GET', 'POST'))
@login_required
def responses(question_id, classname):
    if request.method == 'GET':
        db = get_db()
        question = db.execute(
            'SELECT content, q_type'
            ' FROM question' 
            ' WHERE id = ?',
            (question_id,)
        ).fetchone()
        Q_type =question[1]
        content = question[0]
        if Q_type== "multiple-choice":
            print("multiple choice")
            options = db.execute (
                'SELECT label, content, numChosen FROM options WHERE question_id = ?',   
                (question_id,)
                ).fetchall()
            return render_template('review/mcresponses.html', question = content, options = options)
            
        responses = db.execute(
            'SELECT id, content, created, question_id'
            ' FROM response' #r JOIN user u ON c.teacher = r.id'
            ' WHERE question_id = ?'
            ' ORDER BY created DESC',
            (question_id,)
            ).fetchall()
    

    return render_template('review/responses.html', responses = responses, question = content)


@bp.route("/<question_id>/<options>/mcresponses")
@login_required
def mcresponses(question, options):
    for option in options:
        print(option[0])
    return render_template('review/mcresponses.html', question = question, options = options)


@bp.route('/create')
@login_required
def create():

    return render_template('review/create.html')

@bp.route('/createlongresponse', methods=('GET', 'POST'))
@login_required
def createlongresponse():
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
            'INSERT INTO question (author_id, q_type, content, classname) VALUES (?, ?, ?, ?)',   
            (g.user['id'], 'long response',text, classname)
            )
            db.commit()
            print(classname)
            return redirect(url_for('review.classroom', classname = classname))
        flash(error)
    return render_template('review/createlongresponse.html')

@bp.route('/CreateMultipleChoice', methods=('GET', 'POST'))
@login_required
def CreateMultipleChoice():
    if request.method == 'POST':
        form = request.form
        text = form['question-text']
        text = text.strip()
        classname = request.form['class']
        classname = classname.strip()
        db = get_db()
        error = None
        if not text:
            error = 'You didn\'t add any new question.'
        if error is None:
            db.execute(
            'INSERT INTO question (author_id, q_type, content, classname) VALUES (?, ?, ?, ?)',   
            (g.user['id'], 'multiple-choice', text, classname)

            )
            db.commit()
            q_id  = db.execute(
                'SELECT MAX(id) FROM question',  
               
                )
            Q_id = -1
            for q in q_id:
                Q_id=q[0]
           
            addOptions( 'A', Q_id)
            addOptions( 'B', Q_id)
            addOptions( 'C', Q_id)
            addOptions( 'D', Q_id)
            addOptions( 'E', Q_id)
            return redirect(url_for('review.classroom', classname = classname))
    #if request.method == 'GET':
        
        
    return render_template('review/CreateMultipleChoice.html')

def addOptions(letter, q_id):
    if request.method == 'POST':
        content = request.form[letter]
        content = content.strip()
        db = get_db()
        if content:
            db.execute(
            'INSERT INTO options (question_id, label, content, numChosen) VALUES (?, ?, ?, ?)',   
            (q_id, letter, content, 0)
            )
            db.commit()


@bp.route('/<question_id>/<q_type>/<q_content>/<classname>/response', methods=('GET', 'POST'))
@class_required
def response(question_id, q_type, q_content, classname):
    if request.method == 'GET':
        db = get_db()
        # questions = db.execute(
        #     'SELECT content, q_type FROM question WHERE id = ?',   
        #     (question_id,)
        #     )
        # q_type = ""
        # q_content = ""
        # for q in questions:
        #     q_content = q[0]
        #     print("content " + content)
        #     q_type = q[1]
        if q_type == "multiple-choice":
            print("mc if")
            # options= db.execute(
            # 'SELECT label, content FROM options WHERE question_id = ?',   
            # (question_id,)
            # ).fetchall()
            return redirect(url_for('review.mcresponse', question = q_content, id=question_id, options = "option", classname = classname))

    if request.method == 'POST':
        db = get_db()
        text = request.form['response-text']
        text = text.strip()
        error = None
        if not text:
            error = 'You didn\'t add any new response.'
        if error is None:
            print(text)
            db.execute(
            'INSERT INTO response (content, question_id) VALUES (?, ?)',   
            (text, question_id)
            )
            print(text)
            db.commit()
            return redirect(url_for('review.studentclassroom', classname = classname))
        flash(error)
    
    return render_template('review/response.html', question_id = question_id, q_type = q_type, q_content = q_content, classname = classname )

@bp.route('/<question>/<id>/<options>/<classname>/mcresponse', methods=('GET', 'POST'))
@class_required
def mcresponse(question, id, options, classname):
        
    if request.method == 'GET':
        db = get_db()
        options= db.execute(
            'SELECT label, content, numChosen FROM options WHERE question_id = ?',   
            (id,)
            ).fetchall()
    if request.method == 'POST':
        choice =request.form['customRadio']
        print(choice)
            
        error = None
        
        if not choice:
            error = 'You didn\'t make a choice.'
        if error is None:
            db = get_db()
            db.execute(
            'UPDATE options SET numChosen = numChosen + 1 WHERE label =(?)  AND question_id =(?)',   
            (choice,id)
            )
            db.commit()
            return redirect(url_for('review.studentclassroom', classname = classname))
        flash(error)
    
    return render_template('review/mcresponse.html', question = question , id=id, options = options, classname = classname)


def mcresponse(question, id, options, classname):
    print(option['label'])


@bp.route('/<page_name>')
def other_page(page_name):
    response = make_response(render_template('review/404.html'), 404)
    return response



if __name__ == '__main__':
    app.run(debug=True)
