GET_BUSES_INSIDE_FLEETS = """SELECT
    Bus.id_flotte,
    Bus.id_bus,
    Bus.id_modele_bus,
    SUM(C.kilometres_parcourus) AS distance_totale,
    AVG(C.kilometres_parcourus) AS distance_mensuelle,
    SUM(C.consommation_hydrogene) AS conso_totale,
    AVG(C.consommation_hydrogene) AS conso_moyenne,
    COUNT(C.id_date) AS nombre_pleins
FROM Bus
LEFT JOIN Consomme C ON C.id_bus = Bus.id_bus
GROUP BY Bus.id_bus;"""

GET_FLEETS = """SELECT id_flotte, nom_flotte FROM Flotte;"""
