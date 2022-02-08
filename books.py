
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from auth import get_db, login_required
from app import db

bp = Blueprint("books", __name__)


@bp.route("/books", methods=['GET', 'POST'])
def index():
    """Show all the books, first 20 by id ordering"""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
                SELECT book.isbn, book.title, book.author, book.year
                FROM book ORDER BY book.id ASC LIMIT 20;
    ''')
    books = cur.fetchall()

    for book in books:
        isbn = books[0]
        title = books[1]
        author = books[2]
        year = books[3]


    if request.method == "GET":
        #param = request.form['search']
        param = request.args.get('search', False)
        #param = request.args['search']
        error = None
        
        if not param:
            error = """You have not submitted a query. Enter Search/Query String. 
                        Query cannot be executed for Nonetype Value."""
            
        if error is not None:
            flash(error)
        else:
            #return redirect('/search/'+param)
            cur.execute('''
                        SELECT book.isbn, book.title, book.author, book.year, book.id
                        FROM book WHERE book.title ILIKE %s OR book.isbn ILIKE %s OR book.author ILIKE %s
                        ''', ('%'+param+'%', '%'+param+'%', '%'+param+'%',)
                        )
            bookSearch = cur.fetchall()
            return render_template("books/index.html", bookSearch=bookSearch, param=param,)

    return render_template("books/index.html", 
                            books=books,
                            isbn=isbn,
                            title=title,
                            author=author,
                            year=year,

                            book=book,
                            )


def get_book(isbn):
    """Get a book by isbn.
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT book.isbn, book.title, book.author, book.year, book.id
        FROM book WHERE book.isbn=%s
        ''', (isbn,),)
    book = cur.fetchone()

    if book is None:
        abort(404, f"This book doesn't exist.")

    return book


def get_reviews(book_id):
    #book = get_book(isbn)
    #book_id = book[4]
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT review.text, review.rating, review.book_id, review.person_id
        FROM review WHERE review.book_id=%s
        ''', (book_id,),)
    reviews = cur.fetchall()
    return reviews

def get_reviewer(person_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT person.username
        FROM person WHERE person.id=%s
        ''', (person_id,),)
    reviews = cur.fetchall()
    return reviews    



@bp.route("/<isbn>/details", methods=['GET', 'POST'])
#@login_required
def book_detail(isbn):
    book = get_book(isbn)
    book_id = book[4]
    reviews = get_reviews(book_id)
    uname = None
    if reviews:
        for x in reviews:
            uname = get_reviewer(x[3])

    #reviewer = get_reviewer(person_id)

    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT review.person_id
        FROM review WHERE review.book_id=%s
        ''', (book_id,),)
    rev = cur.fetchall()
    reviewed_users = [x for y in rev for x in y]
    if request.method == 'POST':
        rating = request.form['rating']
        comments = request.form['comments']
        error = None
        if not comments:
            error = "Enter comments"
        if not rating:
            error = "Select a rating"
        if g.person is None:
            return redirect(url_for('auth.login'))
        if g.person[0] in reviewed_users:
            error = """You have already submitted a review for this book. 
                        Multiple Reviews for the same book are not permitted"""
        if error is not None:
            flash(error)
        else:
            conn = get_db()
            cur = conn.cursor()
            cur.execute('''
                    INSERT INTO review (text, rating, book_id, person_id) VALUES (%s, %s, %s, %s)''',
                    (comments, rating, book_id, g.person[0]),)
            conn.commit()
            cur.close()

            return redirect(url_for('books.book_detail', isbn=isbn))
    return render_template("books/detail.html", book=book, reviews=reviews, uname=uname) #reviewer=reviewer)

#Not In Use for now
@bp.route('/search', methods=['GET', 'POST'])
@bp.route('/search/<query>', methods=['GET', 'POST'])
def search(query=None):
    conn = get_db()
    cur = conn.cursor()
    param = query

    if param:
        cur.execute('''
                SELECT book.isbn, book.title, book.author, book.year, book.id
                FROM book WHERE book.title ILIKE %s
                ''', (param+'%',)
                )
        bookSearch = cur.fetchall()
        return render_template("books/index.html", bookSearch=bookSearch, param=param,)
    else:
        if request.method == "POST":
            param = request.form['search']
            error = None

            if not param:
                error = """You have not submitted a query. Enter Search/Query String. 
                            Query cannot be executed for Nonetype Value."""
                
            if error is not None:
                flash(error)
            else:
                cur.execute('''
                            SELECT book.isbn, book.title, book.author, book.year, book.id
                            FROM book WHERE book.title ILIKE %s
                            ''', (param+'%',)
                            )
                bookSearch = cur.fetchall()
                return render_template("books/index.html", bookSearch=bookSearch, param=param,)
    return render_template("books/index.html")