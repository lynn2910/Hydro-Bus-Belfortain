GET_BUSES_INSIDE_FLEETS = """SELECT
    Bus.id_flotte,
    Bus.id_bus,
    Bus.id_modele_bus,
    Bus.nom_bus,
    Bus.date_achat_bus,
    SUM(COALESCE(C.kilometres_parcourus, 0)) AS distance_totale,
    AVG(COALESCE(C.kilometres_parcourus, 0)) AS distance_mensuelle,
    SUM(COALESCE(C.consommation_hydrogene, 0)) AS conso_totale,
    AVG(COALESCE(C.consommation_hydrogene, 0)) AS conso_moyenne,
    COUNT(C.id_date) AS nombre_pleins
FROM Bus
LEFT JOIN Consomme C ON C.id_bus = Bus.id_bus
GROUP BY Bus.id_bus;"""

GET_FLEETS = """SELECT id_flotte, nom_flotte FROM Flotte;"""
GET_BUS_MODELS = """SELECT id_modele_bus, nom_modele_bus, nb_places_bus FROM Modele_bus;"""


INSERT_NEW_BUS = """INSERT INTO Bus (nom_bus, date_achat_bus, id_flotte, id_modele_bus) VALUE (%s, %s, %s, %s);"""
DELETE_BUS = """DELETE FROM Bus WHERE id_bus = %s;"""

GET_BUS_NAME = """SELECT nom_bus FROM Bus WHERE id = %s;"""
