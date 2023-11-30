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

GET_BUS_NAME = """SELECT nom_bus FROM Bus WHERE id_bus = %s;"""

EDIT_BUS = """UPDATE Bus
SET
    nom_bus = %s,
    date_achat_bus = %s,
    id_flotte = %s,
    id_modele_bus = %s
WHERE
    id_bus = %s;"""


GET_BUSES_STATE = """SELECT
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
WHERE
    (Bus.nom_bus LIKE %s)
    AND (Bus.date_achat_bus BETWEEN %s AND %s)
    AND Bus.id_modele_bus = IFNULL(%s, Bus.id_modele_bus)
    AND Bus.id_flotte = IFNULL(%s, Bus.id_flotte)
GROUP BY
    Bus.id_bus
HAVING
    (
        SUM(COALESCE(C.kilometres_parcourus, 0)) >= %s
        AND SUM(COALESCE(C.kilometres_parcourus, 0)) <= %s
    ) AND (
        AVG(COALESCE(C.consommation_hydrogene, 0)) >= %s
        AND AVG(COALESCE(C.consommation_hydrogene, 0)) <= %s
    );"""





GET_BUSES = """SELECT Bus.id_bus, Bus.nom_bus FROM Bus;"""

GET_RESERVOIRS_INSIDE_BUSES = """SELECT
    Reservoir.id_reservoir,
    Reservoir.id_bus,
    Reservoir.id_modele_reservoir,
    Reservoir.taille_reservoir,
    Reservoir.position_dans_bus,
    Reservoir.date_mise_service,
    Reservoir.date_retrait_service,
    Reservoir.nb_cycles_reels,
    COUNT(C.id_controle) AS nb_controle
FROM Reservoir
LEFT JOIN Controle AS C ON C.id_reservoir = Reservoir.id_reservoir
WHERE Reservoir.id_bus IS NOT NULL
GROUP BY
    Reservoir.id_reservoir,
    Reservoir.id_bus,
    Reservoir.id_modele_reservoir,
    Reservoir.taille_reservoir,
    Reservoir.position_dans_bus,
    Reservoir.date_mise_service,
    Reservoir.date_retrait_service,
    Reservoir.nb_cycles_reels;"""

GET_RESERVOIRS_WITHOUT_BUS = """SELECT
    Reservoir.id_reservoir,
    Reservoir.id_bus,
    Reservoir.id_modele_reservoir,
    Reservoir.taille_reservoir,
    Reservoir.position_dans_bus,
    Reservoir.date_mise_service,
    Reservoir.date_retrait_service,
    Reservoir.nb_cycles_reels,
    COUNT(C.id_controle) AS nb_controle
FROM Reservoir
LEFT JOIN Controle AS C ON C.id_reservoir = Reservoir.id_reservoir
WHERE Reservoir.id_bus IS NULL
GROUP BY
    Reservoir.id_reservoir,
    Reservoir.id_bus,
    Reservoir.id_modele_reservoir,
    Reservoir.taille_reservoir,
    Reservoir.position_dans_bus,
    Reservoir.date_mise_service,
    Reservoir.date_retrait_service,
    Reservoir.nb_cycles_reels;
"""

GET_RESERVOIRS_MODELS = """SELECT
    Modele_reservoir.id_modele_reservoir,
    Modele_reservoir.modele_reservoir
FROM Modele_reservoir;"""

GET_RESERVOIRS_POSITION = """SELECT
    Reservoir.position_dans_bus
FROM Reservoir;"""