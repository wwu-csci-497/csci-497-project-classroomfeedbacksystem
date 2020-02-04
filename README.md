# csci-497-project-classroomfeedbacksystem

NIMBLEKNOW: A classoom feedback system 

# clone the repository
$ git clone git@github.com:wwu-csci-497/csci-497-project-classroomfeedbacksystem.git
$ cd csci-497-project-classroomfeedbacksystem

# Create a virtualenv and activate it:

$ python3 -m venv venv 
$ . venv/bin/activate 

Or on Windows cmd: 
$ py -3 -m venv venv
$ venv\Scripts\activate.bat

Install Flaskr:
$ pip install -e .
Or if you are using the master branch, install Flask from source before installing Flaskr:

$ pip install -e ../..
$ pip install -e .

# Run
$ export FLASK_APP=flaskr
$ export FLASK_ENV=development
$ flask init-db
$ flask run

Or on Windows cmd:
$ set FLASK_APP=flaskr
$ set FLASK_ENV=development
$ flask init-db
$ flask run
Open http://127.0.0.1:5000 in a browser.

# Test
$ pip install pytest coverage
$ pytest

# Structure
mean-review-collector
---app
  ---templates
        --base.html
      auth
        --login.html
        --register.html
      review
        --home.html
       --about.html
       --error.html
  ---__init__.py
  ---errors.py
  ---auth.py
  ---review.py
  ---db.py
  ---schema.sql
---tests
---instance
  ---app.sqlite
---env

