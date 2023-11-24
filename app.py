from flask import Flask, render_template, g
import pymysql.cursors

import db
import requests

app = Flask(__name__)
app.secret_key = "e%3v*/=Nj8Zbzz=$bqr1DA$BM7V6/sgWiFD7/NUa6F$psx3wZC6zr~C8MxGAM)#F"


def get_db():
    """
    Establish and return a connection to the MySQL database.
    This function uses the PyMySQL library to establish a connection,
    with connection parameters such as the host, user, password, and database specified.

    The connection uses the 'utf8mb4' charset and DictCursor for cursor-class, which returns rows
    from the database as dictionaries instead of tuples.

    If a connection (denoted as 'db') does not exist in the current application context (g), a new
    connection is established.

    Once established, the connection is saved in the application context to be reused
    on subsequent database queries in the same request.

    :return: The MySQL database connection
    """
    if 'db' not in g:
        g.db = pymysql.connect(
            host=db.HOST,
            user=db.USER,
            password=db.PASSWORD,
            database=db.DATABASE,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/')
def home():
    return render_template('layout.html')


@app.route('/reservoirs/show')
def show_reservoirs():
    return render_template('show_reservoirs.html')


@app.route('/consommation/show')
def modeles_reservoirs():
    return render_template('show_consommation.html')


@app.route('/flottes_bus/show')
def show_flottes_bus():
    return render_template('show_flottes_bus.html')


@app.route('/controles/show')
def show_controles():
    return render_template('show_controles.html')


if __name__ == '__main__':
    app.run()
