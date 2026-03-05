"""Application Streamlit principale."""
import streamlit as st
import os

# Configuration de la page
st.set_page_config(
    page_title="Application de Gestion de Données",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Page d'accueil
st.title("📊 Application de Gestion de Données")

st.markdown("""
## Bienvenue !

Cette application permet de gérer des données via une interface conviviale.

### Fonctionnalités :

- **🔢 Insérer des données** : Ajoutez de nouvelles valeurs numériques avec descriptions
- **📖 Lire les données** : Consultez toutes les données enregistrées

### Comment utiliser cette application :

1. Utilisez la barre latérale pour naviguer entre les pages
2. Sur la page **Insert**, saisissez vos données et soumettez-les
3. Sur la page **Read**, visualisez toutes les données enregistrées

### Architecture :

- **Frontend** : Streamlit (cette application)
- **Backend** : API FastAPI
- **Base de données** : PostgreSQL (avec persistance)

---

👈 **Commencez en sélectionnant une page dans la barre latérale**
""")

# Informations de connexion
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Informations")
api_url = os.getenv("API_URL", "http://localhost:8000")
st.sidebar.info(f"API: {api_url}")
st.sidebar.success("✅ Application prête")
