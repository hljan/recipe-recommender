from flask import Blueprint, render_template, redirect, url_for, request
from models import get_users

# from flask_login import login_required

auth = Blueprint('auth', __name__)


@auth.route('/', methods=['GET', 'POST'])
def login():
    users = get_users()
    if request.method == 'GET':
        return render_template('login.html', user_ids=users['id(u)'])
    elif request.method == 'POST':
        # TODO: add login function here
        userid = '152374'
        return redirect(url_for('main.initial_search', user_id=userid))


@auth.route('/logout')
# @login_required
def logout():
    return redirect(url_for('auth.login'))
