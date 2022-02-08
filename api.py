from flask import Blueprint, jsonify, g, redirect, render_template, request, url_for, flash
#from flask import flash
#from flask import g
#from flask import redirect
#from flask import render_template
#from flask import request
#from flask import url_for
from werkzeug.exceptions import abort
from auth import get_db, login_required
from app import db
import requests
import json



bp = Blueprint("api", __name__)


def book_api(isbn):
    isbn = str(isbn)
    x = 'isbn:' + isbn
    res  =  requests.get("https://www.googleapis.com/books/v1/volumes",  params={"q":  x})
    resj = res.json()
    return resj


@bp.route('/books/api/v1')
def api():
    return render_template("api/api.html",)    


@bp.route('/books/api/v1/<isbn>', methods=("GET", "POST"))
def book_json(isbn):
    #isbn = request.form['search']
    #isbn = request.args.get('search')
    resj = book_api(isbn)
    title = resj['items'][0]['volumeInfo']['title']
    author = resj['items'][0]['volumeInfo']['authors'][0]
    pub_date = resj['items'][0]['volumeInfo']['publishedDate']
    ISBN_10 = resj['items'][0]['volumeInfo']['industryIdentifiers'][0]['identifier']
    ISBN_13 = resj['items'][0]['volumeInfo']['industryIdentifiers'][1]['identifier']
    reviewCount = resj['items'][0]['volumeInfo']['ratingsCount']
    avgRating = resj['items'][0]['volumeInfo']['averageRating']


    return jsonify(title=title,
                    author=author,
                    publishedDate=pub_date,
                    ISBN_10=ISBN_10,
                    ISBN_13=ISBN_13,
                    reviewCount=reviewCount,
                    averageRating=avgRating,)
