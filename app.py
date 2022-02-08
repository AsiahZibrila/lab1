from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
#import config

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Person, Book, Review


#app.add_url_rule('/', endpoint='index')

@app.route('/')
def hello():
    return "<h1>Hello World!</h1>"


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


'''
import auth, api, books
app.register_blueprint(auth.bp)
app.register_blueprint(books.bp)
app.register_blueprint(api.bp)
app.add_url_rule('/', endpoint='index')

'''

if __name__ == '__main__':
    app.run()