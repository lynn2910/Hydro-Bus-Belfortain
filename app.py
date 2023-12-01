import datetime

from flask import Flask, render_template, g, request, redirect, flash
import pymysql.cursors

import db
import requests

app = Flask(__name__)
app.secret_key = "e%3v*/=Nj8Zbzz=$bqr1DA$BM7V6/sgWiFD7/NUa6F$psx3wZC6zr~C8MxGAM)#F"

app.config['TEMPLATES_AUTO_RELOAD'] = True


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
    cursor = get_db().cursor()
    cursor.execute(requests.GET_BUSES)
    buses = cursor.fetchall()

    cursor.execute(requests.GET_RESERVOIRS_INSIDE_BUSES)
    reservoirs_bus = cursor.fetchall()

    cursor.execute(requests.GET_RESERVOIRS_WITHOUT_BUS)
    reservoirs = cursor.fetchall()

    cursor.execute(requests.GET_RESERVOIRS_MODELS)
    modeles_reservoirs = cursor.fetchall()

    cursor.execute(requests.GET_RESERVOIRS_POSITION)
    positions = cursor.fetchall()

    return render_template(
        'reservoirs/show_reservoirs.html',
        buses=buses,
        reservoirs_bus=reservoirs_bus,
        reservoirs=reservoirs,
        modeles_reservoirs=modeles_reservoirs,
        positions=positions
    )


@app.route('/reservoirs/new', methods=["POST"])
def new_reservoir():
    cursor = get_db().cursor()

    # Retrieve form data
    id_bus = int(request.form['id_bus']) if 'id_bus' in request.form and request.form['id_bus'] != '' else None
    date_mise_service = request.form['date_mise_service']
    date_retrait_service = request.form['date_retrait_service'] if 'date_retrait_service' in request.form else None
    taille_reservoir = request.form['taille_reservoir']
    id_modele_reservoir = request.form['id_modele_reservoir']
    position_dans_bus = request.form['position_dans_bus'] if 'position_dans_bus' in request.form else None
    nb_cycles_reels = request.form['nb_cycles_reels']

    # Execute the SQL query
    cursor.execute(requests.INSERT_NEW_RESERVOIR, (
        id_bus,
        date_mise_service,
        None if date_retrait_service is None or date_retrait_service == '' else date_retrait_service,
        taille_reservoir,
        id_modele_reservoir,
        position_dans_bus,
        nb_cycles_reels
    ))

    # Commit the changes to the database
    get_db().commit()

    return redirect('/reservoirs/show')


@app.route('/reservoirs/delete', methods=["GET"])
def delete_reservoir():
    # Retrieve form data from request.args
    id_reservoir = request.args.get('id_reservoir')

    print(id_reservoir)

    # TODO : ajouter message flash
    # https://cours-info.iut-bm.univ-fcomte.fr/upload/perso/77/rs_S1_BDD/bdd1/S1_BDD_pymysql_tp2_flask.html

    cursor = get_db().cursor()
    # Delete associated controle records
    cursor.execute(requests.DELETE_CONTROLES, id_reservoir)
    # Delete the reservoir
    cursor.execute(requests.DELETE_RESERVOIR, id_reservoir)

    get_db().commit()

    return redirect('/reservoirs/show')


@app.route('/reservoirs/edit', methods=["POST"])
def edit_reservoir():
    cursor = get_db().cursor()

    # Retrieve form data
    id_bus = request.form['id_bus'] if 'id_bus' in request.form else None
    id_reservoir = request.form['id_reservoir']
    date_mise_service = request.form['date_service_' + id_reservoir]
    date_retrait_service = request.form[
        'date_retrait_' + id_reservoir] if 'date_retrait_' + id_reservoir in request.form else None
    taille_reservoir = request.form['taille_reservoir_' + id_reservoir]
    id_modele_reservoir = request.form['modele_reservoir_' + id_reservoir]
    position_dans_bus = request.form[
        'position_reservoir_' + id_reservoir] if 'position_reservoir_' + id_reservoir in request.form else None
    nb_cycles_reels = request.form['cycle_reel_' + id_reservoir]

    # TODO : ajouter print + ajouter message flash
    # https://cours-info.iut-bm.univ-fcomte.fr/upload/perso/77/rs_S1_BDD/bdd1/S1_BDD_pymysql_tp2_flask.html

    # Edit in the database
    cursor.execute(requests.EDIT_RESERVOIR, (
        None if id_bus is None or id_bus == '' else id_bus,
        date_mise_service,
        None if date_retrait_service is None or date_retrait_service == '' else date_retrait_service,
        taille_reservoir,
        id_modele_reservoir,
        position_dans_bus,
        nb_cycles_reels,
        id_reservoir
    ))

    get_db().commit()

    return redirect('/reservoirs/show')


@app.route('/reservoirs/etat')
def etat_reservoirs():
    return render_template('reservoirs/etat_reservoirs.html')


@app.route('/consommation/show')
def modeles_reservoirs():
    return render_template('consommation/show_consommation.html')


@app.route('/flottes_bus/show')
def show_flottes_bus():
    cursor = get_db().cursor()
    cursor.execute(requests.GET_BUSES_INSIDE_FLEETS)
    buses = cursor.fetchall()

    cursor.execute(requests.GET_FLEETS)
    fleets = cursor.fetchall()

    cursor.execute(requests.GET_BUS_MODELS)
    bus_models = cursor.fetchall()

    prepared_fleets = []
    for fleet in fleets:
        fleet_buses = []
        for bus in buses:
            if bus["id_flotte"] == fleet["id_flotte"]:
                fleet_buses.append(bus)
        prepared_fleets.append({
            "id_flotte": fleet["id_flotte"],
            "nom_flotte": fleet["nom_flotte"],
            "buses": fleet_buses
        })

    return render_template(
        'bus/show_flottes_bus.html',
        flottes=prepared_fleets,
        bus_models=bus_models,
        add_nom_bus=request.args.get("nom_bus", ''),
        add_date_service=request.args.get("date_service", ''),
        add_id_flotte=request.args.get("nom_bus", ''),
    )


@app.route('/flottes_bus/bus/new', methods=["POST"])
def create_bus():
    nom_bus = request.form.get("nom_bus", "")
    if len(nom_bus) < 1:
        flash("Le nom du bus doit être précisé", "error")
        return redirect('/flottes_bus/show')

    date_achat = request.form.get("date_service", "")
    try:
        datetime.datetime.strptime(date_achat, '%Y-%m-%d')
    except ValueError:
        flash("La date de service n'est pas en format correct, elle doit être au format YYYY-MM-DD", "error")
        return redirect(f'/flottes_bus/show?nom_bus={nom_bus}')

    id_flotte = int(request.form.get("id_flotte", -1))
    if id_flotte < 0:
        flash("La flotte n'existe pas. Veillez à sélectionner une flotte", "error")
        return redirect(f'/flottes_bus/show?nom_bus={nom_bus}&date_service={date_achat}')

    id_modele_bus = int(request.form.get("id_modele_bus", -1))

    if id_modele_bus < 0:
        flash("Le modèle de bus n'existe pas. Veillez à sélectionner un modèle de bus", "error")
        return redirect(f'/flottes_bus/show?nom_bus={nom_bus}&date_service={date_achat}&id_flotte={id_flotte}')

    # Add to database
    cursor = get_db().cursor()
    cursor.execute(requests.INSERT_NEW_BUS, (nom_bus, date_achat, id_flotte, id_modele_bus))

    get_db().commit()

    flash(f"Les modifications du bus '{nom_bus}' ont été appliquées.", "success")

    return redirect('/flottes_bus/show')


@app.route('/flottes_bus/bus/delete', methods=["GET"])
def delete_bus():
    id_bus = request.args.get("id_bus_delete", -1)

    print(id_bus)

    cursor = get_db().cursor()
    # Get bus name
    cursor.execute(requests.GET_BUS_NAME, id_bus)
    bus_name = cursor.fetchone() or {"nom_bus": f"ID({id_bus})"}

    # Delete from database
    try:
        cursor.execute(requests.DELETE_BUS, id_bus)
        get_db().commit()

        flash(f"Le bus {bus_name['nom_bus']} a été supprimé.", "success")

        return redirect('/flottes_bus/show')
    except pymysql.err.IntegrityError:
        flash(f"Le bus {bus_name['nom_bus']} ne peut pas être supprimé.\nVeillez à supprimer ou dé-lier tout réservoir associé à ce bus.", "error")

        return redirect('/flottes_bus/show')


@app.route('/flottes_bus/bus/edit', methods=["POST"])
def edit_bus():
    id_bus = request.form.get("id_bus", -1)

    id_flotte = int(request.form.get("id_flotte", -1))

    if id_flotte < 0:
        flash("La flotte n'existe pas. Veillez à sélectionner une flotte", "error")
        return redirect('/flottes_bus/show')

    id_modele_bus = int(request.form.get("id_modele_bus", -1))

    if id_modele_bus < 0:
        flash("Le modèle de bus n'existe pas. Veillez à sélectionner un modèle de bus", "error")
        return redirect('/flottes_bus/show')

    date_service = request.form.get("date_service", "")

    try:
        datetime.datetime.strptime(date_service, '%Y-%m-%d')
    except ValueError:
        flash("La date de service n'est pas en format correct, elle doit être au format YYYY-MM-DD", "error")
        return redirect('/flottes_bus/show')

    nom_bus = request.form.get("nom_bus", "")

    if len(nom_bus) < 1:
        flash("Le nom du bus doit être précisé", "error")
        return redirect('/flottes_bus/show')

    # Edit in the database
    cursor = get_db().cursor()
    cursor.execute(requests.EDIT_BUS, (nom_bus, date_service, id_flotte, id_modele_bus, id_bus))
    get_db().commit()

    flash(f"Les modifications du bus {nom_bus} ont été effectuées.", "success")

    return redirect('/flottes_bus/show')


@app.route('/flottes_bus/etat')
def etat_flottes_bus():
    filter_word = request.args.get("filter_word")

    date_achat_min = request.args.get("date_achat_min")
    date_achat_max = request.args.get("date_achat_max")

    distance_totale_min = request.args.get("distance_totale_min")
    distance_totale_max = request.args.get("distance_totale_max")

    bus_model = request.args.get("modele_bus") or None
    flotte = request.args.get("flotte") or None

    conso_mensuelle_min = request.args.get("conso_mensuelle_min")
    conso_mensuelle_max = request.args.get("conso_mensuelle_max")

    cursor = get_db().cursor()
    cursor.execute(
        requests.GET_BUSES_STATE,
        (
            f"%{filter_word}%" if filter_word is not None else "%",
            date_achat_min or "1990-01-01",
            date_achat_max or "3000-01-01",
            bus_model,
            flotte,
            int(distance_totale_min) if distance_totale_min else 0,
            int(distance_totale_max) if distance_totale_max else 200000000000,
            int(conso_mensuelle_min) if conso_mensuelle_min else 0,
            int(conso_mensuelle_max) if conso_mensuelle_max else 200000000000
        )
    )
    buses = cursor.fetchall()

    cursor.execute(requests.GET_FLEETS)
    fleets = cursor.fetchall()

    cursor.execute(requests.GET_BUS_MODELS)
    bus_models = cursor.fetchall()

    return render_template(
        'bus/etat_bus.html',
        buses=buses,
        bus_models=bus_models,
        flottes=fleets,
        # Filter
        filter_word=filter_word or "",
        date_achat_min=date_achat_min or '',
        date_achat_max=date_achat_max or '',
        bus_model=bus_model or '',
        flotte_filter=flotte or '',
        distance_totale_min=distance_totale_min or '',
        distance_totale_max=distance_totale_max or '',
        conso_mensuelle_min=conso_mensuelle_min or '',
        conso_mensuelle_max=conso_mensuelle_max or ''
    )


@app.route('/controles/show')
def show_controles():
    return render_template('controles/show_controles.html')


@app.route('/controles/etat')
def etat_controles():
    return render_template('controles/etat_controles.html')


@app.route('/consommation/show')
def show_consommation():
    return render_template('consommation/show_consommation.html')


if __name__ == '__main__':
    app.run()
