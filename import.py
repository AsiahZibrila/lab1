import psycopg2
import csv
#from werkzeug.security import check_password_hash, generate_password_hash

#conn = psycopg2.connect(database="realpy", user="postgres", password="postgres", host="localhost", port="5432")
#cur = conn.cursor()
#cur.execute("INSERT INTO person (username, password) VALUES (%s, %s)", (username, generate_password_hash(password)),)
#cur.execute("INSERT INTO review (text, rating, person_id, book_id) VALUES (%s, %s, %s, %s)", ('great book', 5, 1, 25)
sql_query = "INSERT INTO book (isbn, title, author, year) VALUES (%s, %s, %s, %s)"
#(username, generate_password_hash(password)),
file = r'books.csv'

def get_db():
    conn = psycopg2.connect(database="realpy", 
                            user="postgres", 
                            password="postgres", 
                            host="localhost", 
                            port="5432")
                            
    return conn

try:
    conn = get_db()
    cur = conn.cursor()
    with open('books.csv', 'r') as f:
        lines = csv.reader(f)
        next(lines)
        for line in lines:
            cur.execute(sql_query, line)
            conn.commit()
except (Exception, psycopg2.Error) as e:
    print(e)
finally:
    if (conn):
        cur.close()
        conn.close()
