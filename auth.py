import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
#from app import get_db
from app import db
from models import Person
from psycopg2.errors import UniqueViolation
import psycopg2

def get_db():
    conn = psycopg2.connect(database="books", 
                            user="postgres", 
                            password="postgres", 
                            host="localhost", 
                            port="5432")
                            
    return conn


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db()
        cur = conn.cursor()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                #db.session.execute(
                cur.execute(
                    "INSERT INTO person (username, password) VALUES (%s, %s)",
                    (username, generate_password_hash(password)),
                )
                #db.session.commit()
                conn.commit()
                cur.close()
                conn.close()
            except UniqueViolation:
                error = f"Username {username} is already registered by another user."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db()
        cur = conn.cursor()
        error = None
        cur.execute("SELECT * FROM person WHERE username=%s", (username,))

        person = cur.fetchone()
        if person is None:
            error = 'Invalid username.'
        elif not check_password_hash(person[2], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['person_id'] = person[0]
            return redirect(url_for('books.index'))

        flash(error)
        cur.close()
        conn.close()
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    conn = get_db()
    cur = conn.cursor()
    person_id = session.get('person_id')

    if person_id is None:
        g.person = None
    else:
        cur.execute('SELECT * FROM person WHERE id = %s', (person_id,))
        g.person = cur.fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.person is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view






