DROP TABLE IF EXISTS Controle;
DROP TABLE IF EXISTS Reservoir;
DROP TABLE IF EXISTS Modele_reservoir;
DROP TABLE IF EXISTS Consomme;
DROP TABLE IF EXISTS Mois;
DROP TABLE IF EXISTS Bus;
DROP TABLE IF EXISTS Modele_bus;
DROP TABLE IF EXISTS Flotte;

CREATE TABLE Mois(
   id_mois INT,
   date_plein DATE,
   PRIMARY KEY(id_mois)
);

CREATE TABLE Flotte(
   id_flotte INT AUTO_INCREMENT,
   nom_flotte VARCHAR(50) NOT NULL,
   nb_bus_flotte INT,
   PRIMARY KEY(id_flotte)
);

CREATE TABLE Modele_bus(
   id_modele_bus INT AUTO_INCREMENT,
   nom_modele_bus VARCHAR(50),
   nb_places_bus INT,
   consommation_hydrogene_effective DECIMAL(9,2), -- La consommation en kilogrammes d'hydrogène pour 100 kilomètres
   PRIMARY KEY(id_modele_bus)
);

CREATE TABLE Modele_reservoir(
   id_modele_reservoir INT AUTO_INCREMENT,
   modele_reservoir VARCHAR(50),
   nb_cycles_effectifs INT,
   PRIMARY KEY(id_modele_reservoir)
);

CREATE TABLE Bus(
   id_bus INT AUTO_INCREMENT,
   nom_bus VARCHAR(50),
   date_achat_bus VARCHAR(50),
   id_flotte INT NOT NULL,
   id_modele_bus INT NOT NULL,
   PRIMARY KEY(id_bus),
   FOREIGN KEY(id_flotte) REFERENCES Flotte(id_flotte),
   FOREIGN KEY(id_modele_bus) REFERENCES Modele_bus(id_modele_bus)
);

CREATE TABLE Reservoir(
   id_reservoir INT AUTO_INCREMENT,
   taille_reservoir DECIMAL(7,3),
   position_dans_bus VARCHAR(50),
   date_mise_service DATE,
   date_retrait_service DATE,
   nb_cycles_reels INT,
   id_bus INT,
   id_modele_reservoir INT NOT NULL,
   PRIMARY KEY(id_reservoir),
   FOREIGN KEY(id_bus) REFERENCES Bus(id_bus),
   FOREIGN KEY(id_modele_reservoir) REFERENCES Modele_reservoir(id_modele_reservoir)
);

CREATE TABLE Controle (
   id_controle INT AUTO_INCREMENT,
   date_controle DATE,
   analyse_rendue VARCHAR(200),
   id_reservoir INT NOT NULL,
   PRIMARY KEY(id_controle),
   FOREIGN KEY(id_reservoir) REFERENCES Reservoir(id_reservoir)
);

CREATE TABLE Consomme(
   id_bus INT,
   id_consomme INT AUTO_INCREMENT,
   consommation_hydrogene DECIMAL(9,2),
   kilometres_parcourus DECIMAL(9,2),
   PRIMARY KEY(id_bus, id_consomme),
   FOREIGN KEY(id_bus) REFERENCES Bus(id_bus),
   FOREIGN KEY(id_consomme) REFERENCES Mois(id_mois)
);


#
#
# Jeu de test
#
#

INSERT INTO Flotte
    (id_flotte, nom_flotte, nb_bus_flotte)
VALUE
    (1, 'Makna', 3),
    (2, 'Argentum', 3);

INSERT INTO Modele_bus
    (id_modele_bus, nom_modele_bus, nb_places_bus, consommation_hydrogene_effective)
VALUE
    (1, 'Aegis', 33, 10.0),
    (2, 'Fonsett', 41, 12.0);

INSERT INTO Bus
    (id_bus, nom_bus, date_achat_bus, id_flotte, id_modele_bus)
VALUES
    (1, 'Makna 1', '2021-03-21', 1, 1),
    (2, 'Makna 2', '2022-04-12', 1, 1),
    (3, 'Argentum 1', '2022-09-30', 2, 2);

INSERT INTO Modele_reservoir
    (id_modele_reservoir, modele_reservoir, nb_cycles_effectifs)
VALUE
    (1, 'Alcamoth', 15000),
    (2, 'Tephra', 17000);

INSERT INTO Reservoir
    (id_reservoir, taille_reservoir, position_dans_bus, date_mise_service, date_retrait_service, nb_cycles_reels, id_bus, id_modele_reservoir)
VALUES
    # Bus n°1
    ( 1,  7, 0, '2021-03-21', NULL,         14934, 1, 1),
    ( 2,  7, 0, '2021-03-21', NULL,         14946, 1, 1),
    ( 3,  7, 0, '2023-09-14', NULL,           324, 1, 1),
    ( 4,  7, 0, '2021-03-21', NULL,         14812, 1, 1),
    ( 5,  7, 0, '2021-03-21', NULL,         14843, 1, 1),
    ( 6, 11, 0, '2021-03-21', '2023-09-10', 16723, 1, 2),
    # Bus n°2
    ( 7,  7, 0, '2022-04-12', NULL,         12597, 2, 1),
    ( 8,  7, 0, '2022-04-12', NULL,         12327, 2, 1),
    ( 9,  7, 0, '2022-04-12', NULL,         12349, 2, 1),
    (10,  7, 0, '2022-04-12', NULL,         12534, 2, 1),
    (11,  7, 0, '2022-04-12', NULL,         12567, 2, 1),
    # Bus n°3
    (12, 11, 0, '2022-09-30', NULL,          6621, 3, 2),
    (13, 11, 0, '2021-08-01', NULL,          8651, 3, 1),
    (14, 11, 0, '2021-08-01', NULL,          8349, 3, 1),
    (15, 11, 0, '2022-09-30', NULL,          8629, 3, 2),
    (16, 11, 0, '2022-09-30', NULL,          6627, 3, 2);

INSERT INTO Controle
    (date_controle, analyse_rendue, id_reservoir)
VALUES
    ('2023-09-10', 'Le réservoir est en fin de vie, il ne fonctionne plus qu\'à 14% de ses capacités initiales. Je recommande l\'achat d\'un réservoir de la dernière génération', 5),
    ('2023-07-06', 'Ce réservoir semble être un fin de vie, cependant il est encore fonctionnel à 46% de ses capacités, son changement sera nécessaire dans les prochains mois.', 1),
    ('2022-12-21', 'Aucun problème n\'est à signaler sur ce réservoir.', 3);


INSERT INTO Mois
    (id_mois, date_plein)
VALUES
    (1, '2023-05-01'),
    (2, '2023-02-01'),
    (3, '2023-03-01');

INSERT INTO Consomme
    (id_bus, id_consomme, consommation_hydrogene, kilometres_parcourus)
VALUES
    (1, 1, 210, 2100),
    (1, 2, 215.6, 2156),
    (1, 3, 364.2, 3642);


#
#
# Requêtes
#
#

-- Obtenir les modèles de bus par flotte
-- Cette requête permet d'obtenir la composition d'une flotte
SELECT
    Flotte.id_flotte,
    Flotte.nom_flotte,
    mb.nom_modele_bus,
    COUNT(B.id_bus) AS nombre_bus
FROM
    Flotte
LEFT JOIN Bus B on Flotte.id_flotte = B.id_flotte
LEFT JOIN Modele_bus mb on B.id_modele_bus = mb.id_modele_bus
GROUP BY Flotte.id_flotte, Flotte.nom_flotte, mb.nom_modele_bus;


-- Obtenir tout les contrôles de réservoirs d'un bus
SELECT
    c.id_controle,
    Bus.id_bus,
    c.analyse_rendue,
    c.date_controle
FROM
    Bus
INNER JOIN Reservoir R on Bus.id_bus = R.id_bus
INNER JOIN Controle c on R.id_reservoir = c.id_reservoir
GROUP BY c.id_controle;


-- Obtenir la consommation effective d'une flotte (prévision)
-- Cette requête permet de déterminer la consommation prévisionnelle pour une flotte
SELECT
    Flotte.id_flotte,
    Flotte.nb_bus_flotte,
    mb.consommation_hydrogene_effective * Flotte.nb_bus_flotte
        AS consommation_effective
FROM
    Flotte
LEFT JOIN Bus b on Flotte.id_flotte = b.id_flotte
LEFT JOIN Modele_bus mb on b.id_modele_bus = mb.id_modele_bus
GROUP BY Flotte.id_flotte, b.id_modele_bus;


-- Obtenir la consommation réelle d'un bus pour chaque mois
SELECT
    Bus.id_flotte,
    Bus.id_bus,
    Bus.nom_bus,
    c.consommation_hydrogene,
    c.kilometres_parcourus,
    m.date_plein
FROM
    Bus
LEFT JOIN Consomme c on Bus.id_bus = c.id_bus
LEFT JOIN Mois m on c.id_consomme = m.id_mois;

-- Obtenir la consommation réelle et le kilométrage (moyenne de tout les mois) pour chaque bus
SELECT
    Bus.id_flotte,
    Bus.id_bus,
    Bus.nom_bus,
    AVG(c.consommation_hydrogene) as consommation_hydrogene,
    AVG(c.kilometres_parcourus) as kilometres_parcourus
FROM
    Bus
LEFT JOIN Consomme c on Bus.id_bus = c.id_bus
LEFT JOIN Mois m on c.id_consomme = m.id_mois
GROUP BY Bus.id_flotte, Bus.id_bus, Bus.nom_bus;

-- Obtenir la consommation en hydrogène d'une flotte
SELECT
    Bus.id_flotte,
    AVG(c.consommation_hydrogene)
        AS moyenne_consommation_hydrogene,
    AVG(c.kilometres_parcourus)
       AS moyenne_kilometres_parcourus
FROM Flotte
LEFT JOIN Bus on Bus.id_flotte = Flotte.id_flotte
LEFT JOIN Consomme c on Bus.id_bus = c.id_bus
LEFT JOIN Mois m on c.id_consomme = m.id_mois
GROUP BY Flotte.id_flotte;


-- Avoir le nombre de bus pour chaque modèle de bus
SELECT
    Modele_bus.id_modele_bus,
    Modele_bus.nom_modele_bus,
    COUNT(B.id_bus)
        AS nb_bus
FROM Modele_bus
LEFT JOIN Bus B on Modele_bus.id_modele_bus = B.id_modele_bus
GROUP BY Modele_bus.id_modele_bus;




