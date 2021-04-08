from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

auth = Blueprint('auth', __name__)


@auth.route('/')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST', 'GET'])
def login_post():
    return 'Logged in'


@auth.route('/logout')
# @login_required
def logout():
    return 'Logged out'
