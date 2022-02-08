from app import db
from sqlalchemy.dialects.postgresql import JSON


class Person(db.Model):
    #__tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text(), nullable=False, unique=True)
    #email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)
    reviews = db.relationship('Review', backref='review_user', lazy=True)

    def __repr__(self):
        return '<User: {}>'.format(self.username)


class Book(db.Model):
    #__tablename__ = 'book'
    #__table_args__ = {'schema': 'book_schema'}

    id = db.Column(db.Integer(), primary_key=True)
    isbn = db.Column(db.Text(), unique=True)
    title = db.Column(db.Text())
    author = db.Column(db.Text())
    year = db.Column(db.Integer())
    reviews = db.relationship('Review', backref='reviewed_book', lazy=True)

    def __repr__(self):
        return '<Book: {}>'.format(self.title)


class Review(db.Model):
    #__tablename__ = 'review'

    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.Text())
    rating = db.Column(db.Integer)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))

    def __repr__(self):
        return '<Review {}>'.format(self.text)


