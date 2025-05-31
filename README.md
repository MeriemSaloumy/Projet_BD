

# 🗃️ Projet Bases de Données — Licence MIP – IAP S4

## 📌 Objectif

Ce projet met en œuvre les connaissances acquises en modélisation, en SQL, en algèbre relationnelle, ainsi qu'en développement d'interface avec Python, SQLite et Streamlit. Il est composé de deux parties :

1. **Création et interrogation d'une base MySQL à partir d'un MCD**
2. **Exploitation de la base via une interface Web avec SQLite + Streamlit**

---

## 🧱 Partie 1 — Création et interrogation MySQL

### ✅ Étapes réalisées

- Création du schéma relationnel à partir du MCD
- Traduction en MLD puis en SQL (création de tables)
- Insertion des données fournies en annexe
- Requêtes SQL + Algèbre relationnelle :
  - Réservations avec nom du client et ville de l’hôtel
  - Clients résidant à Paris
  - Nombre de réservations par client
  - Nombre de chambres par type
  - Chambres non réservées entre deux dates

### 📁 Fichiers fournis

- `script_creation.sql` : script de création de la base
- `requetes.sql` : script d’insertion des données
- `requêtes_relationnelles.pdf` : requêtes en algèbre relationnelle

---

## 🌐 Partie 2 — Interface Python + SQLite + Streamlit

### ✅ Fonctionnalités de l’interface

- Consulter la liste des clients et des réservations
- Rechercher les chambres disponibles entre deux dates
- Ajouter un nouveau client
- Ajouter une nouvelle réservation

### 🛠️ Technologies utilisées

- Python 3
- SQLite
- Streamlit

### ▶️ Lancement

```bash
streamlit run app.py
```

---

## 📎 Liens

- 📁 [Dépôt GitHub](https://github.com/MeriemSaloumy/Projet_BD/tree/main/.streamlit)  
- 🎥 [Démonstration Vidéo](https://youtu.be/DJ0OvJZKwX4)

---

## 👤 Auteur\


> Salimi Manar - Saloumy Meriem — Licence MIP — IAP S4  
> Encadré par Pr. J. Zahir

