from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = "e%3v*/=Nj8Zbzz=$bqr1DA$BM7V6/sgWiFD7/NUa6F$psx3wZC6zr~C8MxGAM)#F"

# TODO Voir les noms de variables à mettre :/
# FIXME Il faut modifier quand vous êtes sur vos machines
HOST = ""
PASSWORD = ""
DATABASE = ""


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
