-- a. Réservations avec nom du client et ville de l’hôtel
SELECT r.id AS id_reservation, c.nom, h.ville
FROM Reservation r
JOIN Client c ON r.client_id = c.id
JOIN Chambre_Reservee cr ON r.id = cr.reservation_id
JOIN Chambre ch ON cr.chambre_id = ch.id
JOIN Hotel h ON ch.hotel_id = h.id;

-- b. Clients qui habitent à Paris
SELECT * FROM Client WHERE ville = 'Paris';

-- c. Nombre de réservations par client
SELECT c.nom, COUNT(r.id) AS nb_reservations
FROM Client c
LEFT JOIN Reservation r ON c.id = r.client_id
GROUP BY c.nom;

-- d. Nombre de chambres par type
SELECT t.nom, COUNT(ch.id) AS nb_chambres
FROM TypeChambre t
LEFT JOIN Chambre ch ON t.id = ch.type_id
GROUP BY t.nom;

-- e. Chambres non réservées entre deux dates
-- (exemple : entre '2025-07-01' et '2025-07-10')
SELECT * FROM Chambre
WHERE id NOT IN (
    SELECT cr.chambre_id
    FROM Chambre_Reservee cr
    JOIN Reservation r ON cr.reservation_id = r.id
    WHERE r.date_debut < '2025-07-10' AND r.date_fin > '2025-07-01'
);
