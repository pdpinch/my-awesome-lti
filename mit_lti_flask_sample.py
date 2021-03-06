from flask import Flask, session, request
from flask import render_template
from flask.ext.wtf import Form
from wtforms import IntegerField, BooleanField
from random import randint

from pylti.flask import lti

VERSION = '0.0.1'
app = Flask(__name__)
app.config.from_object('config')


class AddFrom(Form):
    p1 = IntegerField('p1')
    p2 = IntegerField('p2')
    result = IntegerField('result')
    correct = BooleanField('correct')

def error(exception=None):
    return render_template('error.html')


@app.route('/is_up', methods=['GET'])
def hello_world(lti=lti):
    return render_template('up.html', lti=lti)


@app.route('/',methods=['GET','POST'])
@app.route('/index', methods=['GET'])
@app.route('/lti/', methods=['GET','POST'])
@lti(request='initial', error=error, app=app)
def index(lti=lti):
    return render_template('index.html', lti=lti)

@app.route('/index_staff',methods=['GET','POST'])
@lti(request='session', error=error, roles='staff', app=app)
def index_staff(lti=lti):
    return render_template('staff.html', lti=lti)


@app.route('/add', methods=['GET'])
@lti(request='session', error=error, app=app)
def add_form(lti=lti):
    form = AddFrom()
    form.p1.data = randint(1, 9)
    form.p2.data = randint(1, 9)
    return render_template('add.html', form=form)


@app.route('/grade', methods=['POST'])
@lti(request='session', error=error, app=app)
def grade(lti=lti):
    form = AddFrom()
    correct = ((form.p1.data + form.p2.data) == form.result.data)
    form.correct.data = correct
    lti.post_grade(1 if correct else 0)
    return render_template('grade.html', form=form)

def set_debugging():
    import logging
    import sys

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

set_debugging()

if __name__ == '__main__':
#    set_debugging()
    app.run(debug=True)
