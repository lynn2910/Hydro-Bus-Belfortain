from flask import Flask, render_template, g
import pymysql.cursors

app = Flask(__name__)
app.secret_key = "e%3v*/=Nj8Zbzz=$bqr1DA$BM7V6/sgWiFD7/NUa6F$psx3wZC6zr~C8MxGAM)#F"

# TODO Voir les noms de variables à mettre :/
# FIXME Il faut modifier quand vous êtes sur vos machines
HOST = "localhost"
USER = "lynn"
PASSWORD = "Pusyux8484"  # Ce mot de passe est évidemment faux, je ne suis pas fou
DATABASE = "hydrobus_belfortain"


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
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
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
    return render_template('reservoirs/show_reservoirs.html')


@app.route('/reservoirs/models')
def modeles_reservoirs():
    return render_template('reservoirs/modeles_reservoirs.html')


@app.route('/flottes_bus/show')
def show_flottes_bus():
    return render_template('flottes_bus/show_flottes_bus.html')


@app.route('/flottes_bus/models')
def modeles_bus():
    return render_template('flottes_bus/modeles_bus.html')


@app.route('/controles/show')
def show_controles():
    return render_template('controles/show_controles.html')


if __name__ == '__main__':
    app.run()
