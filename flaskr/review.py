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
if __name__ == '__main__':
    app.run(debug=True)