from .models import User, get_todays_recent_recipes
from flask import Flask, request, session, redirect, url_for, render_template, flash

app = Flask(__name__)


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if len(username) < 1:
            flash('Your username must be at least one character.')
        elif len(password) < 5:
            flash('Your password must be at least 5 characters.')
        elif not User(username).register(password):
            flash('A user with that username already exists.')
        else:
            session['username'] = username
            flash('Logged in.')
            return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not User(username).verify_password(password):
            flash('Invalid login.')
        else:
            session['username'] = username
            flash('Logged in.')
            return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    name = request.form['name']

    if not name:
        flash('Your recipe must have a name.')
    else:
        User(session['username']).add_recipe(name)

    return redirect(url_for('index'))


@app.route('/like_recipe/<recipe_id>')
def like_recipe(recipe_id):
    username = session.get('username')

    if not username:
        flash('You must be logged in to like a recipe.')
        return redirect(url_for('login'))

    User(username).like_recipe(recipe_id)

    flash('Liked recipe.')
    return redirect(request.referrer)

@app.route('/profile/<username>')
def profile(username):
    logged_in_username = session.get('username')
    user_being_viewed_username = username

    user_being_viewed = User(user_being_viewed_username)
    recipes = user_being_viewed.get_recent_recipes()

    similar = []
    common = []

    if logged_in_username:
        logged_in_user = User(logged_in_username)

        if logged_in_user.username == user_being_viewed.username:
            similar = logged_in_user.get_similar_users()
        else:
            common = logged_in_user.get_commonality_of_user(user_being_viewed)

    return render_template(
        'profile.html',
        username=username,
        recipes=recipes,
        similar=similar,
        common=common
    )

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    flash('Logged out.')
    return redirect(url_for('index'))