import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
import pandas as pd

# PAGE CONFIGURATION
st.set_page_config(page_title="Hotel Manager", layout="wide")

# ---------------- STYLE CSS ----------------
st.markdown("""
<style>
    .stButton>button {
        border-radius: 8px;
        background-color: #4CAF50;
        color: white;
        padding: 0.4rem 1rem;
        font-weight: bold;
        border: none;
        transition: background 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .metric {
        font-size: 1.2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- BDD ----------------
conn = sqlite3.connect("hotel_data.db")
cur = conn.cursor()

# ---------------- SIDEBAR MENU ----------------
with st.sidebar:
    selected = option_menu(
        menu_title="Menu",
        options=[
            "Accueil", "Réservations", "Clients", "Chambres", 
            "Disponibilités", "Ajouter Client", "Ajouter Réservation",
            "Prestations", "Modifier Client", "Modifier Réservation"
        ],
        icons=[
            "house", "calendar3", "person", "building", 
            "check-square", "person-plus", "calendar-plus",
            "briefcase", "pencil-square", "calendar-x"
        ],
        menu_icon="cast",
        default_index=0
    )

# ---------------- ACCUEIL ----------------
if selected == "Accueil":
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("<h2 style='text-align: center;'>🏨 Bienvenue dans HotelManager</h2>", unsafe_allow_html=True)

        
        
    st.markdown("### 📊 Statistiques générales")
    col1, col2, col3 = st.columns(3)
    cur.execute("SELECT COUNT(*) FROM Client")
    col1.metric("👥 Clients", cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM Reservation")
    col2.metric("📅 Réservations", cur.fetchone()[0])
    cur.execute("SELECT ROUND(AVG(note), 2) FROM Evaluation")
    note = cur.fetchone()[0] or 0
    col3.metric("⭐ Note moyenne", f"{note}/5")
    st.markdown("### 🏨 Statistique complémentaire")

    cur.execute("""
       SELECT h.ville, COUNT(*) as nb
       FROM Reservation r
       JOIN Chambre_Reservee cr ON cr.reservation_id = r.id
       JOIN Chambre ch ON ch.id = cr.chambre_id
       JOIN Hotel h ON ch.hotel_id = h.id
       GROUP BY h.id
       ORDER BY nb DESC
       LIMIT 1
    """)
    result = cur.fetchone()
    if result:
        st.success(f"🏨 Hôtel le plus actif : **{result[0]}** avec **{result[1]} réservations**")
    else:
       st.info("Aucune réservation enregistrée pour le moment.")


# ---------------- RÉSERVATIONS ----------------
elif selected == "Réservations":
    st.markdown("## 📋 Liste des Réservations")
    cur.execute("SELECT DISTINCT c.nom FROM Reservation r JOIN Client c ON r.client_id = c.id")
    noms = [r[0] for r in cur.fetchall()]
    filtre = st.selectbox("Filtrer par client", ["Tous"] + noms)
    if filtre != "Tous":
        cur.execute("""
            SELECT r.id, c.nom, r.date_debut, r.date_fin
            FROM Reservation r JOIN Client c ON r.client_id = c.id
            WHERE c.nom = ?
        """, (filtre,))
    else:
        cur.execute("""
            SELECT r.id, c.nom, r.date_debut, r.date_fin
            FROM Reservation r JOIN Client c ON r.client_id = c.id
        """)
    df = pd.DataFrame(cur.fetchall(), columns=["ID", "Client", "Début", "Fin"])
    st.dataframe(df, use_container_width=True)

# ---------------- CLIENTS ----------------
elif selected == "Clients":
    st.markdown("## 👤 Liste des Clients")
    search = st.text_input("Rechercher un client")
    if search:
        cur.execute("SELECT id, nom, email, ville FROM Client WHERE nom LIKE ?", ('%' + search + '%',))
    else:
        cur.execute("SELECT id, nom, email, ville FROM Client")
    df = pd.DataFrame(cur.fetchall(), columns=["ID", "Nom", "Email", "Ville"])
    st.dataframe(df, use_container_width=True)

# ---------------- CHAMBRES ----------------
elif selected == "Chambres":
    st.markdown("## 🛏️ Liste des Chambres")
    cur.execute("""
        SELECT ch.id, ch.numero, ch.etage, ch.balcon, t.nom, h.ville
        FROM Chambre ch
        JOIN TypeChambre t ON ch.type_id = t.id
        JOIN Hotel h ON ch.hotel_id = h.id
    """)
    df = pd.DataFrame(cur.fetchall(), columns=["ID", "Numéro", "Étage", "Balcon", "Type", "Hôtel"])
    st.dataframe(df)

# ---------------- DISPONIBILITÉS ----------------
elif selected == "Disponibilités":
    st.markdown("## ✅ Chambres disponibles")
    date1 = st.date_input("Date début")
    date2 = st.date_input("Date fin")
    cur.execute("""
        SELECT * FROM Chambre WHERE id NOT IN (
            SELECT chambre_id FROM Chambre_Reservee cr
            JOIN Reservation r ON r.id = cr.reservation_id
            WHERE r.date_debut < ? AND r.date_fin > ?
        )
    """, (date2, date1))
    df = pd.DataFrame(cur.fetchall(), columns=["ID", "Numéro", "Étage", "Balcon", "Type ID", "Hôtel ID"])
    st.dataframe(df)

# ---------------- AJOUT CLIENT ----------------
elif selected == "Ajouter Client":
    st.markdown("## ➕ Ajouter un client")
    with st.form("form_client"):
        nom = st.text_input("Nom")
        email = st.text_input("Email")
        adresse = st.text_input("Adresse")
        ville = st.text_input("Ville")
        code = st.text_input("Code Postal")
        tel = st.text_input("Téléphone")
        submit = st.form_submit_button("Ajouter")
        if submit:
            cur.execute("INSERT INTO Client(nom, email, adresse, ville, code_postal, telephone) VALUES (?, ?, ?, ?, ?, ?)",
                        (nom, email, adresse, ville, code, tel))
            conn.commit()
            st.success("✅ Client ajouté")

# ---------------- AJOUT RÉSERVATION ----------------
elif selected == "Ajouter Réservation":
    st.markdown("## ➕ Ajouter une réservation")
    with st.form("form_res"):
        client_id = st.number_input("ID client", min_value=1)
        chambre_id = st.number_input("ID chambre", min_value=1)
        debut = st.date_input("Date début")
        fin = st.date_input("Date fin")
        submit = st.form_submit_button("Réserver")
        if submit:
            cur.execute("INSERT INTO Reservation(date_debut, date_fin, client_id) VALUES (?, ?, ?)", (debut, fin, client_id))
            res_id = cur.lastrowid
            cur.execute("INSERT INTO Chambre_Reservee(reservation_id, chambre_id) VALUES (?, ?)", (res_id, chambre_id))
            conn.commit()
            st.success("✅ Réservation enregistrée")

# ---------------- PRESTATIONS ----------------
elif selected == "Prestations":
    st.markdown("## 💼 Prestations")
    cur.execute("SELECT id, description, prix FROM Prestation")
    df = pd.DataFrame(cur.fetchall(), columns=["ID", "Description", "Prix"])
    st.dataframe(df)

# ---------------- MODIF CLIENT ----------------
elif selected == "Modifier Client":
    st.markdown("## ✏️ Modifier ou Supprimer un client")
    cur.execute("SELECT id, nom FROM Client")
    options = [f"{i} - {n}" for i, n in cur.fetchall()]
    choix = st.selectbox("Choisir un client", options)
    if choix:
        id_client = int(choix.split(" - ")[0])
        if st.button("❌ Supprimer"):
            cur.execute("DELETE FROM Client WHERE id = ?", (id_client,))
            conn.commit()
            st.success("Client supprimé.")

# ---------------- MODIF RÉSERVATION ----------------
elif selected == "Modifier Réservation":
    st.markdown("## ✏️ Modifier ou Supprimer une réservation")
    cur.execute("SELECT r.id, c.nom FROM Reservation r JOIN Client c ON r.client_id = c.id")
    options = [f"{i} - {n}" for i, n in cur.fetchall()]
    choix = st.selectbox("Choisir une réservation", options)
    if choix:
        id_resa = int(choix.split(" - ")[0])
        if st.button("❌ Supprimer"):
            cur.execute("DELETE FROM Chambre_Reservee WHERE reservation_id = ?", (id_resa,))
            cur.execute("DELETE FROM Reservation WHERE id = ?", (id_resa,))
            conn.commit()
            st.success("Réservation supprimée.")

# ---------------- FIN ----------------
conn.close()

