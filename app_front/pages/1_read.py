"""Page pour lire et afficher les données."""
import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Lire les Données", page_icon="📖")

st.title("📖 Lire les Données")

# Récupérer l'URL de l'API depuis les variables d'environnement
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.markdown(f"""
Cette page affiche toutes les données enregistrées dans la base de données.

**API utilisée** : `{API_URL}`
""")

# Bouton pour rafraîchir les données
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    refresh = st.button("🔄 Rafraîchir", use_container_width=True)
with col2:
    show_stats = st.checkbox("📊 Statistiques", value=False)

# Paramètres de pagination
with st.expander("⚙️ Paramètres"):
    limit = st.slider("Nombre max de résultats", 10, 100, 50, 10)
    skip = st.number_input("Ignorer les premiers résultats", 0, 1000, 0, 10)

# Récupérer les données
try:
    with st.spinner("Chargement des données..."):
        response = requests.get(
            f"{API_URL}/data",
            params={"limit": limit, "skip": skip},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data:
                # Convertir en DataFrame pour un affichage meilleur
                df = pd.DataFrame(data)
                
                # Formater la colonne created_at
                df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M:%S')
                
                # Afficher les statistiques si demandé
                if show_stats:
                    st.subheader("📊 Statistiques")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total d'entrées", len(data))
                    with col2:
                        st.metric("Valeur moyenne", f"{df['value'].mean():.2f}")
                    with col3:
                        st.metric("Valeur min", f"{df['value'].min():.2f}")
                    with col4:
                        st.metric("Valeur max", f"{df['value'].max():.2f}")
                    
                    st.markdown("---")
                
                # Afficher le tableau
                st.subheader(f"📋 Données ({len(data)} résultat(s))")
                
                # Options d'affichage
                display_mode = st.radio(
                    "Mode d'affichage",
                    ["Tableau", "Cartes", "Détails"],
                    horizontal=True
                )
                
                if display_mode == "Tableau":
                    # Affichage en tableau
                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=False,
                        column_config={
                            "id": st.column_config.NumberColumn("ID", format="%d"),
                            "value": st.column_config.NumberColumn("Valeur", format="%.2f"),
                            "description": st.column_config.TextColumn("Description"),
                            "created_at": st.column_config.TextColumn("Date de création")
                        }
                    )
                    
                    # Option de téléchargement
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Télécharger en CSV",
                        data=csv,
                        file_name=f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                    )
                
                elif display_mode == "Cartes":
                    # Affichage en cartes
                    for item in data:
                        with st.container():
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.markdown(f"### 🔢 Valeur: **{item['value']:.2f}**")
                                if item.get('description'):
                                    st.markdown(f"*{item['description']}*")
                                st.caption(f"📅 Créé le : {item['created_at'][:10]}")
                            with col2:
                                st.metric("ID", item['id'])
                            st.markdown("---")
                
                else:  # Détails
                    # Affichage détaillé
                    for idx, item in enumerate(data, 1):
                        with st.expander(f"📄 Entrée #{item['id']} - Valeur: {item['value']:.2f}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write("**ID:**", item['id'])
                                st.write("**Valeur:**", f"{item['value']:.2f}")
                            with col2:
                                st.write("**Date de création:**", item['created_at'])
                                st.write("**Description:**", item.get('description', 'N/A'))
                
            else:
                st.info("ℹ️ Aucune donnée disponible. Ajoutez des données via la page **Insert**.")
        
        else:
            st.error(f"❌ Erreur {response.status_code}: {response.text}")
            
except requests.exceptions.ConnectionError:
    st.error(f"❌ Impossible de se connecter à l'API ({API_URL})")
    st.info("💡 Assurez-vous que l'API est en cours d'exécution")
except requests.exceptions.Timeout:
    st.error("⏱️ Délai d'attente dépassé")
except Exception as e:
    st.error(f"❌ Erreur inattendue : {str(e)}")

# Section d'informations
with st.expander("ℹ️ Informations"):
    st.markdown("""
    ### À propos de cette page
    
    Cette page récupère les données depuis l'API et les affiche de différentes manières :
    
    - **Tableau** : Vue classique en tableau avec possibilité de télécharger en CSV
    - **Cartes** : Vue en cartes pour une meilleure lisibilité
    - **Détails** : Vue détaillée pour chaque entrée
    
    Les données sont stockées de manière persistante dans PostgreSQL.
    """)

# Vérifier la connexion à l'API
try:
    health_response = requests.get(f"{API_URL}/health", timeout=2)
    if health_response.status_code == 200:
        st.sidebar.success("✅ API connectée")
    else:
        st.sidebar.warning("⚠️ API accessible mais problème")
except:
    st.sidebar.error("❌ API non accessible")
