-- Création de la base MySQL

CREATE TABLE Hotel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ville VARCHAR(100),
    pays VARCHAR(100),
    code_postal VARCHAR(10)
);

CREATE TABLE Client (
    id INT AUTO_INCREMENT PRIMARY KEY,
    adresse VARCHAR(150),
    ville VARCHAR(100),
    code_postal VARCHAR(10),
    email VARCHAR(100),
    telephone VARCHAR(20),
    nom VARCHAR(100)
);

CREATE TABLE Prestation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    prix DECIMAL(5,2),
    description VARCHAR(100)
);

CREATE TABLE TypeChambre (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50),
    prix DECIMAL(6,2)
);

CREATE TABLE Chambre (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(10),
    etage INT,
    balcon BOOLEAN,
    type_id INT,
    hotel_id INT,
    FOREIGN KEY (type_id) REFERENCES TypeChambre(id),
    FOREIGN KEY (hotel_id) REFERENCES Hotel(id)
);

CREATE TABLE Reservation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_debut DATE,
    date_fin DATE,
    client_id INT,
    FOREIGN KEY (client_id) REFERENCES Client(id)
);

CREATE TABLE Chambre_Reservee (
    reservation_id INT,
    chambre_id INT,
    PRIMARY KEY (reservation_id, chambre_id),
    FOREIGN KEY (reservation_id) REFERENCES Reservation(id),
    FOREIGN KEY (chambre_id) REFERENCES Chambre(id)
);

CREATE TABLE Evaluation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_eval DATE,
    note INT CHECK (note BETWEEN 0 AND 5),
    commentaire TEXT,
    reservation_id INT,
    FOREIGN KEY (reservation_id) REFERENCES Reservation(id)
);
