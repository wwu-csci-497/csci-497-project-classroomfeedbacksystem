#review.py
from flask import Flask, render_template, make_response, Blueprint, g


# import more
bp = Blueprint('review', __name__)
@bp.route('/')
def home():
    return render_template('review/home.html')
@bp.route('/question')
def question():
    return render_template('review/question.html')

@bp.route('/about')
def about():
    return render_template('review/about.html')

@bp.route('/<page_name>')
def other_page(page_name):
    response = make_response(render_template('review/404.html'), 404)
    return response

@bp.route('/create', methods=('GET', 'POST'))
#@login_required
def create():
    if request.method == 'POST':
        text = request.form['review-text']
        text = text.strip()
        db = get_db()
        error = None
    if not text:
        error = 'You didn\'t add any new reviews.'
    if error is None:
        db.execute(
            'INSERT INTO question (author_id, content) VALUES (?, ?)',
            (g.user['id'], text)
        )
    db.commit()
    return redirect(url_for('review.dashboard'))

    flash(error)

    return render_template('review/question.html')

if __name__ == '__main__':
    app.run(debug=True)
