#
#
#
#       Petit message à tous ceux qui ouvrira ce fichier
#
# Bonne chance pour naviguer dedans
# L'objectif est d'enregistrer autre-part les requêtes pour ne pas surcharger le fichier `app.py`
#
#
#


SHOW_BUS_MODELS = """SELECT
    Modele_bus.consommation_hydrogene_effective,
    Modele_bus.nb_places_bus,
    Modele_bus.nom_modele_bus,
    Modele_bus.id_modele_bus,
    IFNULL(bus_res.nombre_bus, 0) AS nombre_bus,
    IFNULL(conso.consommation_hydrogene, 0) as consommation_hydrogene,
    IFNULL(conso.kilometres_parcourus, 0) as kilometres_parcourus,
    IFNULL(res.nombre_reservoirs, 0) AS nombre_reservoirs
FROM
    Modele_bus
LEFT JOIN
    (SELECT id_modele_bus, COUNT(id_bus) as nombre_bus
    FROM Bus GROUP BY id_modele_bus) as bus_res
    ON bus_res.id_modele_bus = Modele_bus.id_modele_bus
LEFT JOIN
    (SELECT Bus.id_modele_bus, AVG(c.consommation_hydrogene) as consommation_hydrogene,
     SUM(c.kilometres_parcourus) as kilometres_parcourus
     FROM Consomme c
     INNER JOIN Bus ON c.id_bus = Bus.id_bus
     GROUP BY Bus.id_modele_bus) as conso
    ON conso.id_modele_bus = Modele_bus.id_modele_bus
LEFT JOIN
    (SELECT Bus.id_modele_bus, COUNT(Reservoir.id_reservoir) as nombre_reservoirs
    FROM Reservoir
    INNER JOIN Bus ON Reservoir.id_bus = Bus.id_bus
    GROUP BY Bus.id_modele_bus) as res
    ON res.id_modele_bus = Modele_bus.id_modele_bus;"""
